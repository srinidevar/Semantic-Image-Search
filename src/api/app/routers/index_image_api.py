from fastapi import APIRouter
from fastapi import File, UploadFile
from .image_indexer import get_image_indexer

# Create a FastAPI router for handling image indexing API endpoints
router = APIRouter()

@router.post("/indeximage", tags=["Index images"])
async def index_image(file: UploadFile = File(...)):
    """
    Endpoint to upload and index an image file.

    Args:
        file (UploadFile): The uploaded image file.

    Returns:
        dict: Response indicating success or failure of the operation.
    """
    try:
        # Define the file path where the uploaded file will be saved
        fname = "/home/app/web/data/" + file.filename

        # Save the uploaded file to the specified path in chunks
        with open(fname, 'wb') as f:
            while contents := file.file.read(1024 * 1024):  # Read in 1MB chunks
                f.write(contents)

        # Enqueue the file for indexing by the worker thread
        get_image_indexer().enque(fname)
    except Exception as e:
        # Handle any exceptions that occur during file upload or indexing
        return {"message": "There was an exception uploading the file - " + str(e) + '}'}
    finally:
        # Ensure the file is properly closed after processing
        file.file.close()

    # Return a success response
    return {'response': 'OK'}