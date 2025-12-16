from django.contrib import admin
from .models import Department, Class, Student, Course, Score, Teacher, ClassCourse

# 注册院系模型
@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'updated_at')
    search_fields = ('name',)

# 注册班级模型
@admin.register(Class)
class ClassAdmin(admin.ModelAdmin):
    list_display = ('name', 'department', 'grade', 'major', 'created_at', 'updated_at')
    list_filter = ('department', 'grade', 'major')
    search_fields = ('name',)

# 注册学生模型
@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('student_id', 'name', 'gender', 'class_info', 'admission_date', 'status', 'created_at', 'updated_at')
    list_filter = ('class_info', 'gender', 'status', 'admission_date')
    search_fields = ('student_id', 'name')
    raw_id_fields = ('user',)

# 注册课程模型
@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'department', 'credit', 'created_at', 'updated_at')
    list_filter = ('department', 'credit')
    search_fields = ('code', 'name')

# 注册成绩模型
@admin.register(Score)
class ScoreAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'semester', 'score', 'created_at', 'updated_at')
    list_filter = ('course', 'semester')
    search_fields = ('student__name', 'student__student_id', 'course__name')
    raw_id_fields = ('student', 'course')

# 注册教师模型
@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('teacher_id', 'name', 'gender', 'department', 'created_at', 'updated_at')
    list_filter = ('department', 'gender')
    search_fields = ('teacher_id', 'name')
    raw_id_fields = ('user',)

# 注册班级课程关联模型
@admin.register(ClassCourse)
class ClassCourseAdmin(admin.ModelAdmin):
    list_display = ('class_info', 'course', 'teacher', 'semester', 'created_at', 'updated_at')
    list_filter = ('semester', 'course', 'teacher')
    search_fields = ('class_info__name', 'course__name')
    raw_id_fields = ('class_info', 'course', 'teacher')
