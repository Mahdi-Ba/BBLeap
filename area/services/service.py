from datetime import datetime
import httpx


async def query_stac_api(polygon) -> (str, str):
    search_url = "https://earth-search.aws.element84.com/v0/search"
    headers = {"Content-Type": "application/json"}
    payload = {
        "intersects": polygon,
        "query": {
            "eo:cloud_cover": {
                "lt": 10  # Example: looking for images with less than 10% cloud cover
            }
        },
        "sort": [
            {"field": "datetime", "direction": "desc"}  # Sort results by date, newest first
        ],
        "limit": 1  # Retrieve only the newest image
    }
    async with httpx.AsyncClient() as client:
        response = await client.post(search_url, json=payload, headers=headers, timeout=10)
        response.raise_for_status()  # Raises exception for 4XX/5XX responses
        return response.json()['features'][0].get("assets", {}).get('thumbnail', {}).get('href', ''), \
            response.json()['features'][0].get("properties", {}).get("updated", datetime.utcnow())
