from aiohttp import (
    web,
    ClientSession,
)
import asyncio
import os

from cache import (
    store_cache,
    search,
)
from images_client import fetch_images_data

DEFAULT_REFRESH_PERIOD = 10
DEFAULT_HTTP_HOST = "127.0.0.1"
DEFAULT_HTTP_PORT = 8080
routes = web.RouteTableDef()

@routes.get('/search/{search_term}')
async def hello(request):
    return web.json_response(search(request.match_info['search_term']))

async def fetch_images_periodically():
    while True:
        data = await fetch_images_data(os.getenv("API_KEY"))
        store_cache(data)
        await asyncio.sleep(int(os.getenv("REFRESH_PERIOD", DEFAULT_REFRESH_PERIOD)))

async def start_background_tasks(app):
    asyncio.create_task(fetch_images_periodically())

def main():
    app = web.Application()
    app.add_routes(routes)
    app.on_startup.append(start_background_tasks)
    web.run_app(
        app, 
        host=os.getenv("HTTP_HOST", DEFAULT_HTTP_HOST), 
        port=int(os.getenv("HTTP_PORT", DEFAULT_HTTP_PORT))
    )

if __name__ == '__main__':
    main()
