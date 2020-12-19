from aiohttp import web
from aiohttp.web_request import Request
from .config import db_block, web_routes, render_html


@web_routes.get("/student")
async def view_student_list(request):
    return render_html(request, 'student_list.html')
