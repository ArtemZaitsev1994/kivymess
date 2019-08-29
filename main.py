from aiohttp import web
import json
from datetime import datetime
import collections
import os


def echo(request):
    print(request.headers.get('X-Real-IP'))
    print(request.headers)
    print(dir(request.headers))
    print(dir(request))
    print(request.items())
    return web.Response(text=json.dumps({'hello':'world'}))

app = web.Application()
app.add_routes([
    web.get('/', echo)
])
web.run_app(app, port=os.getenv('PORT'))

if __name__ == '__main__':
    web.run_app(app)