import datetime
from aiohttp import web
from dataclasses import asdict
from serv.json_util import json_dumps

from .config import db_block, web_routes


@web_routes.get("/api/course/list")
async def get_course_list(request):
    with db_block() as db:
        db.execute("""
        SELECT sn AS cou_sn, no AS cou_no, name AS cou_name, term as cou_term, place,time FROM course
        """)
        data = list(asdict(r) for r in db)
        
    return web.Response(text=json_dumps(data), content_type="application/json")


@web_routes.get("/api/course/{cou_sn:\d+}")
async def get_course_profile(request):
    cou_sn = request.match_info.get("cou_sn")

    with db_block() as db:
        db.execute("""
       SELECT sn AS cou_sn, no AS cou_no, name AS cou_name, term, place,time FROM course
        WHERE sn=%(cou_sn)s
        """, dict(cou_sn=cou_sn))
        record = db.fetch_first()

    if record is None:
        return web.HTTPNotFound(text=f"no such course: cou_sn={cou_sn}")

    data = asdict(record)
    return web.Response(text=json_dumps(data), content_type="application/json")


@web_routes.post("/api/course")
async def new_course(request):
    course = await request.json()
   

    with db_block() as db:
        db.execute("""
        INSERT INTO course (term, no, name, place, time)
        VALUES(%(cou_term)s, %(cou_no)s, %(cou_name)s, %(place)s, %(time)s) RETURNING sn;
        """, course)
        record = db.fetch_first()

        course["cou_sn"] = record.sn
    
    print(course)

    return web.Response(text=json_dumps(course), content_type="application/json")


@web_routes.put("/api/course/{cou_sn:\d+}")
async def update_course(request):
    cou_sn = request.match_info.get("cou_sn")

    course = await request.json()
    

    course["cou_sn"] = cou_sn

    with db_block() as db:
        db.execute("""
        UPDATE course SET
            term=%(cou_term)s, no=%(cou_no)s, name=%(cou_name)s,place=%(place)s, time=%(time)s
        WHERE sn=%(cou_sn)s;
        """, course)

    return web.Response(text=json_dumps(course), content_type="application/json")


@web_routes.delete("/api/course/{cou_sn:\d+}")
async def delete_course(request):
    cou_sn = request.match_info.get("cou_sn")
    
    with db_block() as db:
        db.execute("""
        DELETE FROM course WHERE sn=%(cou_sn)s;
       
        """, dict(cou_sn=cou_sn) )

    return web.Response(text="", content_type="text/plain")
