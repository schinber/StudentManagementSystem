from django.urls import path
from . import views

urlpatterns = [
    # 首页
    path('', views.home, name='home'),
    # 学生个人中心
    path('profile/', views.student_profile, name='student_profile'),
    # 学生成绩查询
    path('my-scores/', views.student_scores, name='student_scores'),
    
    # 学生管理
    path('students/', views.student_list, name='student_list'),
    path('students/<int:pk>/', views.student_detail, name='student_detail'),
    path('students/create/', views.student_create, name='student_create'),
    path('students/<int:pk>/update/', views.student_update, name='student_update'),
    path('students/<int:pk>/delete/', views.student_delete, name='student_delete'),
    
    # 课程管理
    path('courses/', views.course_list, name='course_list'),
    path('courses/<int:pk>/', views.course_detail, name='course_detail'),
    path('courses/create/', views.course_create, name='course_create'),
    path('courses/<int:pk>/update/', views.course_update, name='course_update'),
    path('courses/<int:pk>/delete/', views.course_delete, name='course_delete'),
    
    # 成绩管理
    path('scores/', views.score_list, name='score_list'),
    path('scores/<int:pk>/', views.score_detail, name='score_detail'),
    path('scores/create/', views.score_create, name='score_create'),
    path('scores/<int:pk>/update/', views.score_update, name='score_update'),
    path('scores/<int:pk>/delete/', views.score_delete, name='score_delete'),
    
    # 班级管理
    path('classes/', views.class_list, name='class_list'),
    path('classes/<int:pk>/', views.class_detail, name='class_detail'),
    path('classes/create/', views.class_create, name='class_create'),
    path('classes/<int:pk>/update/', views.class_update, name='class_update'),
    path('classes/<int:pk>/delete/', views.class_delete, name='class_delete'),
    
    # 院系管理
    path('departments/', views.department_list, name='department_list'),
    path('departments/<int:pk>/', views.department_detail, name='department_detail'),
    path('departments/create/', views.department_create, name='department_create'),
    path('departments/<int:pk>/update/', views.department_update, name='department_update'),
    path('departments/<int:pk>/delete/', views.department_delete, name='department_delete'),
    
    # 教师管理
    path('teachers/', views.teacher_list, name='teacher_list'),
    path('teachers/<int:pk>/', views.teacher_detail, name='teacher_detail'),
    path('teachers/create/', views.teacher_create, name='teacher_create'),
    path('teachers/<int:pk>/update/', views.teacher_update, name='teacher_update'),
    path('teachers/<int:pk>/delete/', views.teacher_delete, name='teacher_delete'),
]