from django.contrib.auth.models import User
from students.models import Department, Class, Student, Course, Score, Teacher

# 创建测试数据
print("开始创建测试数据...")

# 创建院系
department1 = Department.objects.create(name="计算机学院", description="培养计算机相关专业人才")
department2 = Department.objects.create(name="电子工程学院", description="培养电子工程相关专业人才")
department3 = Department.objects.create(name="经济管理学院", description="培养经济管理相关专业人才")
print("已创建院系数据")

# 创建班级
class1 = Class.objects.create(name="计算机科学与技术1班", department=department1, grade=2023, major="计算机科学与技术")
class2 = Class.objects.create(name="计算机科学与技术2班", department=department1, grade=2023, major="计算机科学与技术")
class3 = Class.objects.create(name="软件工程1班", department=department1, grade=2023, major="软件工程")
class4 = Class.objects.create(name="电子信息工程1班", department=department2, grade=2023, major="电子信息工程")
class5 = Class.objects.create(name="市场营销1班", department=department3, grade=2023, major="市场营销")
print("已创建班级数据")

# 创建课程
course1 = Course.objects.create(name="Python程序设计", code="CS101", department=department1, credit=3.0, description="Python编程语言基础")
course2 = Course.objects.create(name="数据结构", code="CS102", department=department1, credit=4.0, description="数据结构与算法")
course3 = Course.objects.create(name="数据库原理", code="CS103", department=department1, credit=3.5, description="数据库设计与管理")
course4 = Course.objects.create(name="电子电路基础", code="EE101", department=department2, credit=3.0, description="电子电路基本原理")
course5 = Course.objects.create(name="市场营销学", code="MG101", department=department3, credit=2.5, description="市场营销基本理论与实践")
print("已创建课程数据")

# 创建教师
teacher1 = Teacher.objects.create(teacher_id="T001", name="张老师", gender="male", phone="13800138001", email="zhang@example.com", department=department1)
teacher2 = Teacher.objects.create(teacher_id="T002", name="李老师", gender="female", phone="13800138002", email="li@example.com", department=department1)
teacher3 = Teacher.objects.create(teacher_id="T003", name="王老师", gender="male", phone="13800138003", email="wang@example.com", department=department2)
print("已创建教师数据")

print("测试数据创建完成！")