from aiohttp import web
from .config import db_block, web_routes, render_html


@web_routes.get("/")
async def home_page(request):
    return web.HTTPFound(location="/grade")

