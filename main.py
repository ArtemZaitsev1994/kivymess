from aiohttp import web
import json
from datetime import datetime
import collections
import os


def echo(request):
    print(1)
    return web.Response(text=json.dumps(request))

app = web.Application()
app.add_routes([
    web.get('/', echo)
])
web.run_app(app, port=os.getenv('PORT'))

if __name__ == '__main__':
    web.run_app(app)