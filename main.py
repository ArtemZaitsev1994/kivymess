from aiohttp import web
import json
from datetime import datetime
import collections
import os


def echo(request):
    return web.Response(text=json.dumps(request))

app = web.Application()
web.run_app(app, port=os.getenv('PORT', 8000))
app.add_routes([
    web.get('/', echo)
])

if __name__ == '__main__':
    web.run_app(app)