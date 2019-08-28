from aiohttp import web
import json
from datetime import datetime
import collections


def echo(request):
    return web.Response(text=json.dumps(request))

web.run_app(app, port=os.getenv('PORT', 8000))
app = web.Application()
app.add_routes([
    web.get('/', echo)
])

if __name__ == '__main__':
    web.run_app(app)