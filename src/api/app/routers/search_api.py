from fastapi import APIRouter
from .image_indexer import query_image

# Create a FastAPI router for handling image search API endpoints
router = APIRouter()

@router.post("/searchimage/{query}", tags=["Search images"])
async def searchimage(query: str):
    """
    Endpoint to search for images based on a query.

    Args:
        query (str): The search query string.

    Returns:
        dict: Response containing the search result URL or an indication of success.
    """
    # Log the incoming search query
    print("Image search query - ", query)

    # Perform the image search using the query
    resp = query_image(query)

    # Log the response from the image search function
    print("Returning", resp, type(resp))

    # Return the search result as a response
    return {'response': 'OK', "URL": resp}