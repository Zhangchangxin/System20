DELETE FROM course_grade;
DELETE FROM course;
DELETE FROM student;

INSERT INTO student (sn, no, name)  VALUES
    (101, 'S001',  '张三'),
    (102, 'S002',  '李四'), 
    (103, 'S003',  '王五'),
    (104, 'S004',  '马六');


INSERT INTO course (sn, term, no, name, place, time)  VALUES 
    (101,'2020秋季学期', 'C01',  '高数','第一公教A210','周二第一大节'), 
    (102,'2020秋季学期', 'C02',  '外语','第一公教A308','周一第二大节'),
    (103,'2020秋季学期', 'C03',  '线代','第一公教C211','周五第一大节');


INSERT INTO course_grade (stu_sn, cou_sn,term,grade)  VALUES 
    (101, 101,'2020秋季学期',  91), 
    (102, 101,'2020秋季学期', 89),
    (103, 101,'2020秋季学期',  90),
    (101, 102,'2020秋季学期',  89);



INSERT INTO course_choose (stu_sn, cou_sn,term,course_name)  VALUES 
    (101, 101,'2020秋季学期', '高数'), 
    (102, 101,'2020秋季学期','外语'),
    (103, 101,'2020秋季学期', '线代');