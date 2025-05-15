# Semantic Image Search
Text-based image search using OpenCLIP is a form of semantic search through images.

## 1. General Information
### a. How CLIP Enables Semantic Image Search
- Semantic Understanding: CLIP is trained on millions of image-text pairs, learning to map both images and their textual descriptions into a shared high-dimensional vector space. This allows it to capture the meaning (semantics) of both modalities, not just surface features or tags.

- Embedding Space: Both images and text queries are converted into embeddings (vectors). When you perform a search, the model compares the embedding of your text query to the embeddings of images in the database. Images with embeddings closest to the query (by cosine similarity or similar metrics) are returned as the most relevant results.

- Beyond Tags and Metadata: Unlike traditional image search that relies on filenames, tags, or manual annotations, CLIP-based semantic search can retrieve images that match the concept described in the text, even if those exact words or tags are absent from the dataset.

### b. How It Works (Workflow)
- Indexing: Every image in your database is processed by the CLIP model to generate an image embedding, which is stored in a vector database.

- Querying: When a user enters a text query (e.g., “a bike in front of a red brick wall”), the same CLIP model generates a text embedding for the query.

- Similarity Search: The system retrieves images whose embeddings are closest to the query embedding, effectively finding images that are semantically similar to the text input.

## 2. Implementation
### a. Pre-requisites
- Pre-installed docker, docker-compose
- Familiarity with docker and docker-compose

*Note - I used docker desktop version 4.37.2 (179585) on Macbook (Apple Silicon)*

### b. Frameworks Used
- VUEJS for the UI
- FastAPI in the API layer
- Milvus as vector db
- etcd and minio for milvus

## 3. How to Use
### a. Build & Deploy
- Clone the repo and navigate to the 'src' folder and launch the build script. It will recursively build all the 3 images (UI, API, and Image Server). 
- Once the build is complete navigate to the deploy folder and launch the application using the provided docker-compose yaml file. 
- It is assumed that there are no port conflicts. Currently, ports exposed by docker - 3000 (UI), 9999 (Image Server), and 8000 (API). 

    * If you change the UI port no additional required
    * If you change the image server port, remove the docker volumes folder and reindex the image content. 
    * If you change the API port, edit the VUE js files (search all references and update the port numbers)

### b. Use
- Build and launch the app
- Navigate to "Index Image" menu in the sidebar. A few images are included in the repo under "images" folder. Upload these images one after the other for indexing. You can check the indexing progress in the logs (docker logs -f is-api-container). 
- Once all the images are indexed, navigate to the "Image Search" menu ub the sidebar and enter the search queries. For the included images you could use the following search terms. 

    * ysl
    * pink clutch
    * coming soon
    * dark stairwell
    * brown purse
    * IWC

## 4. Improvements/Future Work
Development and testing happened on a macbook. Indexed about 200 images and tested the code without any issues. The search was fast with this workload. The performance limits of this implementation has not been measured. Look at the laundry list before you decide to use this code. 
- Check the perofrmance limits of this code base on a specific hardware configuration
- Optimize docker images
- Python implementation can be improved
- Security hardening
- and a few more...

*Note - I am sharing this code base AS-IS.*
