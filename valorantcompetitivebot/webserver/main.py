from aiohttp import web


async def start():
    app = web.Application()
    app.add_routes(routes)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, host='0.0.0.0', port=80)
    await site.start()


routes = web.RouteTableDef()


@routes.get('/')
async def hello(request):
    return web.Response(text=f"Hello, World!\n{request}")
