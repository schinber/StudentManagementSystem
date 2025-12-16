from django.contrib.auth.models import User
from students.models import Student, Class

def create_test_account():
    print("开始创建测试账户...")
    
    # 检查是否已存在同名用户
    if User.objects.filter(username='testuser').exists():
        print("用户 'testuser' 已存在，正在更新...")
        user = User.objects.get(username='testuser')
        user.set_password('123456')
        user.email = 'test@example.com'
        user.save()
    else:
        # 创建新用户
        print("创建新用户 'testuser'...")
        user = User.objects.create_user(
            username='testuser',
            password='123456',
            email='test@example.com'
        )
    
    # 获取第一个班级
    class_info = Class.objects.first()
    if not class_info:
        print("错误：没有找到班级信息，请先创建班级！")
        return
    
    # 检查是否已存在同名学生
    if Student.objects.filter(student_id='20230001').exists():
        print("学生 '20230001' 已存在，正在更新...")
        student = Student.objects.get(student_id='20230001')
        student.user = user
        student.name = '测试学生'
        student.save()
    else:
        # 创建对应的学生信息
        print("创建学生信息...")
        student = Student.objects.create(
            user=user,
            student_id='20230001',
            name='测试学生',
            gender='male',
            birth_date='2005-01-01',
            phone='13800138001',
            email='test@example.com',
            class_info=class_info,
            admission_date='2023-09-01',
            status='enrolled'
        )
    
    print("测试账户创建成功！")
    print(f"用户名: {user.username}")
    print(f"密码: 123456")
    print(f"学号: {student.student_id}")

if __name__ == "__main__":
    create_test_account()