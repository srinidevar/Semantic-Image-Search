from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import index_image_api, search_api
from contextlib import asynccontextmanager
from .routers.image_indexer import initialize_image_indexer as init_img_indexer
from .routers.image_indexer import get_image_indexer

# Define a lifespan context manager for the FastAPI application
@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Context manager to handle the application's lifespan events.

    This initializes resources when the application starts and
    cleans up resources when the application shuts down.
    """
    print("Initialize ...")
    # Initialize the image indexer when the application starts
    init_img_indexer()
    yield
    # Clean up resources and stop the image indexer when the application shuts down
    print("Reclaim all resources & connections...")
    get_image_indexer().stop()

# Launch the FastAPI application with the defined lifespan
app = FastAPI(lifespan=lifespan)

# Define the list of allowed origins for CORS
origins = [
    "http://localhost:3000",  # Frontend development server
    "http://localhost:3001"  # Alternative frontend server
]

# Add CORS middleware to allow cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allow requests from specified origins
    allow_credentials=True,  # Allow cookies and credentials
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

# Include the routers for image indexing and search APIs
app.include_router(index_image_api.router)
app.include_router(search_api.router)

# Define a default root endpoint
@app.get("/", tags=["Default root page"])
async def root():
    """
    Default root endpoint for the API.

    Returns:
        str: A welcome message for the API.
    """
    return "Image Search Powered by Generative AI"