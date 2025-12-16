from django import forms
from .models import Department, Class, Student, Course, Score, Teacher
from django.contrib.auth.models import User

class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = '__all__'

class ClassForm(forms.ModelForm):
    class Meta:
        model = Class
        fields = '__all__'

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['student_id', 'name', 'gender', 'birth_date', 'phone', 'email', 'address', 'class_info', 'admission_date', 'status']
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date'}),
            'admission_date': forms.DateInput(attrs={'type': 'date'}),
        }

class TeacherForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = ['teacher_id', 'name', 'gender', 'phone', 'email', 'department']

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = '__all__'

class ScoreForm(forms.ModelForm):
    class Meta:
        model = Score
        fields = '__all__'