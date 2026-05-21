import httpx
from fastapi import HTTPException

IN_PLACE_CACHE = {}

async def verify_place_exists(external_id: int) -> bool:
    if external_id in IN_PLACE_CACHE:
        return IN_PLACE_CACHE[external_id]

    url = f"https://api.artic.edu/api/v1/artworks/{external_id}"

    async with httpx.AsyncClient() as client:
        response = await client.get(url)

        if response.status_code == 200:
            IN_PLACE_CACHE[external_id] = True
            return True
        elif response.status_code == 404:
            IN_PLACE_CACHE[external_id] = False
            return False
        else:
            raise HTTPException(status_code=response.status_code, detail=response.text)

