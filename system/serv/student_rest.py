import datetime
from aiohttp import web
from dataclasses import asdict
from serv.json_util import json_dumps

from .config import db_block, web_routes


@web_routes.get("/api/student/list")
async def get_student_list(request):
    with db_block() as db:
        db.execute("""
        SELECT sn AS stu_sn, no AS stu_no, name AS stu_name, gender, enrolled FROM student
        """)
        data = list(asdict(r) for r in db)
        
    return web.Response(text=json_dumps(data), content_type="application/json")


@web_routes.get("/api/student/{stu_sn:\d+}")
async def get_student_profile(request):
    stu_sn = request.match_info.get("stu_sn")

    with db_block() as db:
        db.execute("""
        SELECT sn AS stu_sn, no AS stu_no, name AS stu_name, gender, enrolled FROM student
        WHERE sn=%(stu_sn)s
        """, dict(stu_sn=stu_sn))
        record = db.fetch_first()

    if record is None:
        return web.HTTPNotFound(text=f"no such student: stu_sn={stu_sn}")

    data = asdict(record)
    return web.Response(text=json_dumps(data), content_type="application/json")


@web_routes.post("/api/student")
async def new_student(request):
    student = await request.json()
    if not student.get('enrolled'):
        student['enrolled'] = datetime.date(1900, 1, 1)

    with db_block() as db:
        db.execute("""
        INSERT INTO student (no, name, gender, enrolled)
        VALUES(%(stu_no)s, %(stu_name)s, %(gender)s, %(enrolled)s) RETURNING sn;
        """, student)
        record = db.fetch_first()

        student["stu_sn"] = record.sn
    
    print(student)

    return web.Response(text=json_dumps(student), content_type="application/json")


@web_routes.put("/api/student/{stu_sn:\d+}")
async def update_student(request):
    stu_sn = request.match_info.get("stu_sn")

    student = await request.json()
    if not student.get('enrolled'):
        student['enrolled'] = datetime.date(1900, 1, 1)

    student["stu_sn"] = stu_sn

    with db_block() as db:
        db.execute("""
        UPDATE student SET
            no=%(stu_no)s, name=%(stu_name)s, gender=%(gender)s, enrolled=%(enrolled)s
        WHERE sn=%(stu_sn)s;
        """, student)

    return web.Response(text=json_dumps(student), content_type="application/json")


@web_routes.delete("/api/student/{stu_sn:\d+}")
async def delete_student(request):
    stu_sn = request.match_info.get("stu_sn")

    with db_block() as db:
        db.execute("""
        DELETE FROM student WHERE sn=%(stu_sn)s;
        """, dict(stu_sn=stu_sn))

    return web.Response(text="", content_type="text/plain")
