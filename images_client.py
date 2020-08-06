from aiohttp import (
    ClientSession,
)
import asyncio

API_BASE_URL = "http://interview.agileengine.com:80"
API_AUTH_URI = "/auth"
API_IMAGES_URI = "/images"


async def auth(session: ClientSession, api_key: str) -> str:
    async with session.post(API_BASE_URL + API_AUTH_URI, json={'apiKey': api_key}) as response:
        data = await response.json()
        return data['token']


async def get_page_data(session: ClientSession, token: str, page: int=1) -> dict:
    async with session.get(
        API_BASE_URL + API_IMAGES_URI, 
        params={'page': page}, 
        headers={"Authorization": f"Bearer {token}"}
    ) as response:
        return await response.json()


async def get_full_image_data(session: ClientSession, token: str, image_id: str) -> dict:
    async with session.get(
        f"{API_BASE_URL}{API_IMAGES_URI}/{image_id}", 
        headers={"Authorization": f"Bearer {token}"}
    ) as response:
        return await response.json()

async def fetch_images_data(api_key: str) -> dict:
    async with ClientSession() as session:
        token = await auth(session, api_key)
        first_page = await get_page_data(session, token)
        data = first_page['pictures']
        page_count = first_page['pageCount']
        if page_count > 1:
            other_pages = await asyncio.gather(
                *(get_page_data(session, token, page_number) for page_number in range(1, page_count))
            )
            for page in other_pages:
                data.extend(page['pictures'])
        images_data = await asyncio.gather(
            *(get_full_image_data(session, token, image["id"]) for image in data)
        )
        return images_data
