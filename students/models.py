from django.db import models
from django.contrib.auth.models import User

# 院系模型
class Department(models.Model):
    name = models.CharField(max_length=100, verbose_name='院系名称')
    description = models.TextField(blank=True, verbose_name='院系描述')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = '院系'
        verbose_name_plural = '院系'

# 班级模型
class Class(models.Model):
    name = models.CharField(max_length=100, verbose_name='班级名称')
    department = models.ForeignKey(Department, on_delete=models.CASCADE, verbose_name='所属院系')
    grade = models.IntegerField(verbose_name='年级')
    major = models.CharField(max_length=100, verbose_name='专业')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    
    def __str__(self):
        return f'{self.department.name} - {self.major} - {self.grade}级 - {self.name}'
    
    class Meta:
        verbose_name = '班级'
        verbose_name_plural = '班级'

# 学生模型
class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True, verbose_name='关联用户')
    student_id = models.CharField(max_length=20, unique=True, verbose_name='学号')
    name = models.CharField(max_length=50, verbose_name='姓名')
    gender = models.CharField(max_length=10, choices=[('male', '男'), ('female', '女')], verbose_name='性别')
    birth_date = models.DateField(verbose_name='出生日期')
    phone = models.CharField(max_length=15, blank=True, verbose_name='联系电话')
    email = models.EmailField(blank=True, verbose_name='电子邮箱')
    address = models.TextField(blank=True, verbose_name='家庭住址')
    class_info = models.ForeignKey(Class, on_delete=models.CASCADE, verbose_name='所属班级')
    admission_date = models.DateField(verbose_name='入学日期')
    status = models.CharField(max_length=20, choices=[('enrolled', '在读'), ('graduated', '已毕业'), ('dropped', '已退学')], default='enrolled', verbose_name='学生状态')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    
    def __str__(self):
        return f'{self.student_id} - {self.name}'
    
    class Meta:
        verbose_name = '学生'
        verbose_name_plural = '学生'

# 课程模型
class Course(models.Model):
    name = models.CharField(max_length=100, verbose_name='课程名称')
    code = models.CharField(max_length=20, unique=True, verbose_name='课程代码')
    department = models.ForeignKey(Department, on_delete=models.CASCADE, verbose_name='所属院系')
    credit = models.FloatField(verbose_name='学分')
    description = models.TextField(blank=True, verbose_name='课程描述')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    
    def __str__(self):
        return f'{self.code} - {self.name}'
    
    class Meta:
        verbose_name = '课程'
        verbose_name_plural = '课程'

# 成绩模型
class Score(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, verbose_name='学生')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='课程')
    semester = models.CharField(max_length=20, verbose_name='学期')
    score = models.FloatField(verbose_name='成绩')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    
    def __str__(self):
        return f'{self.student.name} - {self.course.name} - {self.semester} - {self.score}'
    
    class Meta:
        verbose_name = '成绩'
        verbose_name_plural = '成绩'
        unique_together = ('student', 'course', 'semester')

# 教师模型（扩展User模型）
class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='关联用户')
    teacher_id = models.CharField(max_length=20, unique=True, verbose_name='教师工号')
    name = models.CharField(max_length=50, verbose_name='姓名')
    gender = models.CharField(max_length=10, choices=[('male', '男'), ('female', '女')], verbose_name='性别')
    phone = models.CharField(max_length=15, blank=True, verbose_name='联系电话')
    email = models.EmailField(blank=True, verbose_name='电子邮箱')
    department = models.ForeignKey(Department, on_delete=models.CASCADE, verbose_name='所属院系')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    
    def __str__(self):
        return f'{self.teacher_id} - {self.name}'
    
    class Meta:
        verbose_name = '教师'
        verbose_name_plural = '教师'

# 班级课程关联模型（记录哪些班级上哪些课程）
class ClassCourse(models.Model):
    class_info = models.ForeignKey(Class, on_delete=models.CASCADE, verbose_name='班级')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='课程')
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, verbose_name='授课教师')
    semester = models.CharField(max_length=20, verbose_name='学期')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    
    def __str__(self):
        return f'{self.class_info} - {self.course} - {self.semester} - {self.teacher.name}'
    
    class Meta:
        verbose_name = '班级课程'
        verbose_name_plural = '班级课程'
        unique_together = ('class_info', 'course', 'semester')
