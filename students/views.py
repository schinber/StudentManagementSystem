from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Department, Class, Student, Course, Score, Teacher
from .forms import StudentForm, CourseForm, ScoreForm, DepartmentForm, ClassForm, TeacherForm

# 首页视图
@login_required
def home(request):
    return render(request, 'students/home.html')

# 学生个人中心视图
@login_required
def student_profile(request):
    # 获取当前登录用户对应的学生信息
    student = Student.objects.get(user=request.user)
    return render(request, 'students/student_profile.html', {'student': student})

# 学生成绩查询视图
@login_required
def student_scores(request):
    # 获取当前登录用户对应的学生成绩
    student = Student.objects.get(user=request.user)
    scores = student.score_set.select_related('course').all()
    return render(request, 'students/student_scores.html', {'student': student, 'scores': scores})

# 检查用户是否为管理员或教师
from django.contrib.auth.decorators import user_passes_test

def is_admin_or_teacher(user):
    """检查用户是否为管理员或教师"""
    return user.is_superuser or hasattr(user, 'teacher')

# 学生列表视图
@login_required
@user_passes_test(is_admin_or_teacher)
def student_list(request):
    # 使用select_related优化数据库查询，减少N+1查询问题
    students = Student.objects.select_related('class_info', 'class_info__department').all()
    return render(request, 'students/student_list.html', {'students': students})

# 学生详情视图
@login_required
@user_passes_test(is_admin_or_teacher)
def student_detail(request, pk):
    # 使用prefetch_related优化成绩查询
    student = Student.objects.select_related('class_info', 'class_info__department').prefetch_related('score_set', 'score_set__course').get(pk=pk)
    return render(request, 'students/student_detail.html', {'student': student})

# 创建学生视图
@login_required
@user_passes_test(is_admin_or_teacher)
def student_create(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        # 添加调试信息
        print(f"表单数据: {request.POST}")
        print(f"表单是否有效: {form.is_valid()}")
        if form.is_valid():
            try:
                student = form.save(commit=False)
                print(f"学生学号: {student.student_id}")
                print(f"学生邮箱: {student.email}")
                
                # 确保邮箱不为空
                email = student.email if student.email else f"{student.student_id}@example.com"
                
                # 创建一个新的User对象，用户名使用学号
                user = User.objects.create_user(
                    username=student.student_id,
                    password='123456',  # 默认密码
                    email=email
                )
                print(f"创建的User对象: {user}")
                
                student.user = user
                print(f"学生对象的user字段: {student.user}")
                print(f"学生对象的user_id字段: {student.user_id}")
                
                student.save()
                print("学生对象保存成功！")
                
                messages.success(request, '学生信息添加成功！')
                return redirect('student_list')
            except Exception as e:
                print(f"创建学生失败: {e}")
                messages.error(request, f'添加学生失败: {e}')
        else:
            print(f"表单错误: {form.errors}")
            messages.error(request, '表单验证失败，请检查输入的信息！')
    else:
        form = StudentForm()
    return render(request, 'students/student_form.html', {'form': form, 'title': '添加学生'})

# 更新学生视图
@login_required
@user_passes_test(is_admin_or_teacher)
def student_update(request, pk):
    student = Student.objects.get(pk=pk)
    if request.method == 'POST':
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            messages.success(request, '学生信息更新成功！')
            return redirect('student_list')
    else:
        form = StudentForm(instance=student)
    return render(request, 'students/student_form.html', {'form': form, 'title': '更新学生信息'})

# 删除学生视图
@login_required
@user_passes_test(is_admin_or_teacher)
def student_delete(request, pk):
    student = Student.objects.get(pk=pk)
    if request.method == 'POST':
        student.delete()
        messages.success(request, '学生信息删除成功！')
        return redirect('student_list')
    return render(request, 'students/student_confirm_delete.html', {'student': student})

# 课程列表视图
@login_required
@user_passes_test(is_admin_or_teacher)
def course_list(request):
    courses = Course.objects.select_related('department').all()
    return render(request, 'students/course_list.html', {'courses': courses})

# 课程详情视图
@login_required
@user_passes_test(is_admin_or_teacher)
def course_detail(request, pk):
    course = Course.objects.select_related('department').get(pk=pk)
    return render(request, 'students/course_detail.html', {'course': course})

# 创建课程视图
@login_required
@user_passes_test(is_admin_or_teacher)
def course_create(request):
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, '课程信息添加成功！')
            return redirect('course_list')
    else:
        form = CourseForm()
    return render(request, 'students/course_form.html', {'form': form, 'title': '添加课程'})

# 更新课程视图
@login_required
@user_passes_test(is_admin_or_teacher)
def course_update(request, pk):
    course = Course.objects.get(pk=pk)
    if request.method == 'POST':
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            messages.success(request, '课程信息更新成功！')
            return redirect('course_list')
    else:
        form = CourseForm(instance=course)
    return render(request, 'students/course_form.html', {'form': form, 'title': '更新课程信息'})

# 删除课程视图
@login_required
@user_passes_test(is_admin_or_teacher)
def course_delete(request, pk):
    course = Course.objects.get(pk=pk)
    if request.method == 'POST':
        course.delete()
        messages.success(request, '课程信息删除成功！')
        return redirect('course_list')
    return render(request, 'students/course_confirm_delete.html', {'course': course})

# 成绩列表视图
@login_required
@user_passes_test(is_admin_or_teacher)
def score_list(request):
    scores = Score.objects.select_related('student', 'student__class_info', 'course').all()
    return render(request, 'students/score_list.html', {'scores': scores})

# 成绩详情视图
@login_required
@user_passes_test(is_admin_or_teacher)
def score_detail(request, pk):
    score = Score.objects.select_related('student', 'course').get(pk=pk)
    return render(request, 'students/score_detail.html', {'score': score})

# 创建成绩视图
@login_required
@user_passes_test(is_admin_or_teacher)
def score_create(request):
    if request.method == 'POST':
        form = ScoreForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, '成绩信息添加成功！')
            return redirect('score_list')
    else:
        form = ScoreForm()
    return render(request, 'students/score_form.html', {'form': form, 'title': '添加成绩'})

# 更新成绩视图
@login_required
@user_passes_test(is_admin_or_teacher)
def score_update(request, pk):
    score = Score.objects.get(pk=pk)
    if request.method == 'POST':
        form = ScoreForm(request.POST, instance=score)
        if form.is_valid():
            form.save()
            messages.success(request, '成绩信息更新成功！')
            return redirect('score_list')
    else:
        form = ScoreForm(instance=score)
    return render(request, 'students/score_form.html', {'form': form, 'title': '更新成绩信息'})

# 删除成绩视图
@login_required
@user_passes_test(is_admin_or_teacher)
def score_delete(request, pk):
    score = Score.objects.get(pk=pk)
    if request.method == 'POST':
        score.delete()
        messages.success(request, '成绩信息删除成功！')
        return redirect('score_list')
    return render(request, 'students/score_confirm_delete.html', {'score': score})

# 班级列表视图
@login_required
@user_passes_test(is_admin_or_teacher)
def class_list(request):
    classes = Class.objects.select_related('department').all()
    return render(request, 'students/class_list.html', {'classes': classes})

# 班级详情视图
@login_required
@user_passes_test(is_admin_or_teacher)
def class_detail(request, pk):
    class_info = Class.objects.select_related('department').get(pk=pk)
    return render(request, 'students/class_detail.html', {'class_info': class_info})

# 创建班级视图
@login_required
@user_passes_test(is_admin_or_teacher)
def class_create(request):
    if request.method == 'POST':
        form = ClassForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, '班级信息添加成功！')
            return redirect('class_list')
    else:
        form = ClassForm()
    return render(request, 'students/class_form.html', {'form': form, 'title': '添加班级'})

# 更新班级视图
@login_required
@user_passes_test(is_admin_or_teacher)
def class_update(request, pk):
    class_info = Class.objects.get(pk=pk)
    if request.method == 'POST':
        form = ClassForm(request.POST, instance=class_info)
        if form.is_valid():
            form.save()
            messages.success(request, '班级信息更新成功！')
            return redirect('class_list')
    else:
        form = ClassForm(instance=class_info)
    return render(request, 'students/class_form.html', {'form': form, 'title': '更新班级信息'})

# 删除班级视图
@login_required
@user_passes_test(is_admin_or_teacher)
def class_delete(request, pk):
    class_info = Class.objects.get(pk=pk)
    if request.method == 'POST':
        class_info.delete()
        messages.success(request, '班级信息删除成功！')
        return redirect('class_list')
    return render(request, 'students/class_confirm_delete.html', {'class_info': class_info})

# 院系列表视图
@login_required
@user_passes_test(is_admin_or_teacher)
def department_list(request):
    departments = Department.objects.all()
    return render(request, 'students/department_list.html', {'departments': departments})

# 院系详情视图
@login_required
@user_passes_test(is_admin_or_teacher)
def department_detail(request, pk):
    department = Department.objects.get(pk=pk)
    return render(request, 'students/department_detail.html', {'department': department})

# 创建院系视图
@login_required
@user_passes_test(is_admin_or_teacher)
def department_create(request):
    if request.method == 'POST':
        form = DepartmentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, '院系信息添加成功！')
            return redirect('department_list')
    else:
        form = DepartmentForm()
    return render(request, 'students/department_form.html', {'form': form, 'title': '添加院系'})

# 更新院系视图
@login_required
@user_passes_test(is_admin_or_teacher)
def department_update(request, pk):
    department = Department.objects.get(pk=pk)
    if request.method == 'POST':
        form = DepartmentForm(request.POST, instance=department)
        if form.is_valid():
            form.save()
            messages.success(request, '院系信息更新成功！')
            return redirect('department_list')
    else:
        form = DepartmentForm(instance=department)
    return render(request, 'students/department_form.html', {'form': form, 'title': '更新院系信息'})

# 删除院系视图
@login_required
@user_passes_test(is_admin_or_teacher)
def department_delete(request, pk):
    department = Department.objects.get(pk=pk)
    if request.method == 'POST':
        department.delete()
        messages.success(request, '院系信息删除成功！')
        return redirect('department_list')
    return render(request, 'students/department_confirm_delete.html', {'department': department})

# 教师列表视图
@login_required
@user_passes_test(is_admin_or_teacher)
def teacher_list(request):
    teachers = Teacher.objects.select_related('department').all()
    return render(request, 'students/teacher_list.html', {'teachers': teachers})

# 教师详情视图
@login_required
@user_passes_test(is_admin_or_teacher)
def teacher_detail(request, pk):
    teacher = Teacher.objects.select_related('department').get(pk=pk)
    return render(request, 'students/teacher_detail.html', {'teacher': teacher})

# 创建教师视图
@login_required
@user_passes_test(is_admin_or_teacher)
def teacher_create(request):
    if request.method == 'POST':
        form = TeacherForm(request.POST)
        if form.is_valid():
            try:
                teacher = form.save(commit=False)
                # 创建一个新的User对象，用户名使用教师工号
                email = teacher.email if teacher.email else f"{teacher.teacher_id}@example.com"
                user = User.objects.create_user(
                    username=teacher.teacher_id,
                    password='123456',  # 默认密码
                    email=email
                )
                teacher.user = user
                teacher.save()
                messages.success(request, '教师信息添加成功！')
                return redirect('teacher_list')
            except Exception as e:
                messages.error(request, f'添加教师失败: {e}')
    else:
        form = TeacherForm()
    return render(request, 'students/teacher_form.html', {'form': form, 'title': '添加教师'})

# 更新教师视图
@login_required
@user_passes_test(is_admin_or_teacher)
def teacher_update(request, pk):
    teacher = Teacher.objects.get(pk=pk)
    if request.method == 'POST':
        form = TeacherForm(request.POST, instance=teacher)
        if form.is_valid():
            form.save()
            messages.success(request, '教师信息更新成功！')
            return redirect('teacher_list')
    else:
        form = TeacherForm(instance=teacher)
    return render(request, 'students/teacher_form.html', {'form': form, 'title': '更新教师信息'})

# 删除教师视图
@login_required
@user_passes_test(is_admin_or_teacher)
def teacher_delete(request, pk):
    teacher = Teacher.objects.get(pk=pk)
    if request.method == 'POST':
        # 删除关联的User对象
        if teacher.user:
            teacher.user.delete()
        teacher.delete()
        messages.success(request, '教师信息删除成功！')
        return redirect('teacher_list')
    return render(request, 'students/teacher_confirm_delete.html', {'teacher': teacher})
