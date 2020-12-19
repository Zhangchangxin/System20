from aiohttp import web
from aiohttp.web_request import Request
from .config import db_block, web_routes, render_html


@web_routes.get("/course")
async def view_course_list(request):
    return render_html(request, 'course.html')