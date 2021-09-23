
import asyncio

from flask.json import jsonify
from aiohttp import ClientSession
import requests
import json

from init import app


# @app.route('/')
# async def index():
#     await asyncio.sleep(1)
#     return 'Hello'

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36',
    'Content-Type': 'application/json'
}

urls = ['http://localhost:5000/source_a',
        'http://localhost:5000/source_b',
        'http://localhost:5000/source_c']

# Helper Functions

async def fetch_url(session, url):
    """Fetch the specified URL using the aiohttp session specified."""
    async with session.get(url, headers=HEADERS) as response:
        text = await response.text(encoding='utf-8')
        return json.loads(text)


# Routes

@app.route('/async_get')
async def async_get():
    """Asynchronously retrieve the list of URLs."""

    async with ClientSession() as session:
        tasks = []
        for url in urls:
            task = asyncio.create_task(fetch_url(session, url))
            tasks.append(task)
        sites = await asyncio.gather(*tasks)

    # Generate the HTML response
    l = list()
    for site in sites:
        for res in site['results']:
            l.append({'id': res['id'], 'name': res['name']})

    newlist = sorted(l, key=lambda k: int(k['id']))
    return jsonify(newlist)