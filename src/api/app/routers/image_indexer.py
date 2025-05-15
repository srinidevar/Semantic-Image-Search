from queue import Queue
from threading import Thread, Event
from pymilvus import (
    connections,
    utility,
    FieldSchema, CollectionSchema, DataType,
    Collection,
)
import open_clip
from PIL import Image
import os

# Global variables for the indexer, data collection, and model components
indexer = None
data_collection = None
model = None
preprocess = None
tokenizer = None

# Function to query the image database using a text query
def query_image(query):
    # Retrieve the collection, tokenizer, and model for searching
    its_collection, tokenizer, model = get_image_search_trio()
    its_collection.load()  # Load the collection into memory

    # Tokenize and encode the query text
    text = tokenizer(query)
    text_features = model.encode_text(text)
    text_features /= text_features.norm(dim=-1, keepdim=True)  # Normalize the features
    text_features = text_features.reshape((512,))
    text_features = text_features.detach().numpy()

    # Define search parameters for the vector database
    search_params = {
        "metric_type": "L2",
        "params": {"nprobe": 10},
    }

    # Perform the search and retrieve results
    result = its_collection.search([text_features], "image_embeddings", search_params, limit=3, output_fields=["image_source"])

    # Print and return the first result
    for hits in result:
        for hit in hits:
            print(f"hit: {hit}, image source: {hit.entity.get('image_source')}")
    return hits[0].entity.get('image_source')

# Function to index an image into the vector database
def index_image(image_filepath):
    # Generate a URL for the image based on its file path
    imageUrl = image_filepath.replace("/home/app/web/data", "http://localhost:9999")
    print(f"Processing - {image_filepath}/{imageUrl}")

    # Retrieve the collection, preprocessing function, and model for indexing
    its_collection, preprocess, model = get_image_indexing_trio()

    # Preprocess the image and extract its features
    image = preprocess(Image.open(image_filepath)).unsqueeze(0)
    image_features = model.encode_image(image)
    image_features /= image_features.norm(dim=-1, keepdim=True)  # Normalize the features
    image_features = image_features.reshape((512,))
    image_features = image_features.detach().numpy()

    # Prepare the data to be inserted into the vector database
    entities = [
        [imageUrl],
        [image_features]
    ]

    # Insert the data into the collection and flush changes
    insert_result = its_collection.insert(entities)
    its_collection.flush()
    print("Image indexed and added to vector db", insert_result)

# Function to initialize the vector database and model components
def initialize():
    # Load the model and preprocessing functions
    model, _, preprocess = open_clip.create_model_and_transforms('ViT-B-32', pretrained='laion2b_s34b_b79k')
    tokenizer = open_clip.get_tokenizer('ViT-B-32')

    # Connect to the Milvus vector database
    connections.connect(alias='default', host='is-milvus-standalone', port="19530")

    # Define the schema for the collection
    fields = [
        FieldSchema(name="pk", dtype=DataType.INT64, is_primary=True, auto_id=True, max_length=100),
        FieldSchema(name="image_source", dtype=DataType.VARCHAR, max_length=512),
        FieldSchema(name="image_embeddings", dtype=DataType.FLOAT_VECTOR, dim=512)
    ]
    schema = CollectionSchema(fields, "image_text_similarity is the collection for this app")

    # Check if the collection exists, and create it if not
    if not utility.has_collection('image_text_similarity'):
        print('Collection is not available')
        its_collection = Collection("image_text_similarity", schema, consistency_level="Strong")
        index = {
            "index_type": "IVF_FLAT",
            "metric_type": "L2",
            "params": {"nlist": 128},
        }
        its_collection.create_index("image_embeddings", index)
        return its_collection, model, preprocess, tokenizer
    else:
        its_collection = Collection("image_text_similarity", schema, consistency_level="Strong")
        return its_collection, model, preprocess, tokenizer

# Function to initialize the image indexer and related components
def initialize_image_indexer():
    global indexer
    global data_collection
    global model
    global preprocess
    global tokenizer

    # Initialize the worker thread if not already initialized
    if indexer is None:
        indexer = Worker()

    # Initialize the vector database and model components
    data_collection, model, preprocess, tokenizer = initialize()

# Helper function to retrieve the indexer instance
def get_image_indexer():
    global indexer
    return indexer

# Helper function to retrieve the collection, preprocessing function, and model for indexing
def get_image_indexing_trio():
    global data_collection
    global model
    global preprocess
    return data_collection, preprocess, model

# Helper function to retrieve the collection, tokenizer, and model for searching
def get_image_search_trio():
    global data_collection
    global model
    global tokenizer
    return data_collection, tokenizer, model

# Worker class to handle tasks in a separate thread
class Worker(Thread):
    """Thread executing tasks from a given tasks queue"""
    def __init__(self):
        Thread.__init__(self)
        self.abort = Event()  # Event to signal thread termination
        self.queue = Queue()  # Queue to hold tasks
        self.daemon = True  # Set thread as a daemon
        self.start()  # Start the thread

    """Stop the worker thread"""
    def stop(self):
        self.abort.set()

    """Add a task to the queue"""
    def enque(self, fname):
        self.queue.put((fname))

    """Thread work loop calling the function with the params"""
    def run(self):
        # Keep running until told to abort
        while not self.abort.is_set():
            try:
                # Get a task and raise immediately if none available
                image_filepath = self.queue.get()
            except:
                continue

            try:
                # Process the task (index the image)
                print("Worker thread - " + image_filepath)
                index_image(image_filepath)
            except Exception as e:
                print("Exception while calling worker function - " + str(e))
            finally:
                # Mark the task as done
                self.queue.task_done()