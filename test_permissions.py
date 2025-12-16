#!/usr/bin/env python3
"""
测试权限控制脚本
"""

import os
import sys
import django

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'student_management_system.settings')
django.setup()

from django.contrib.auth.models import User
from django.test import Client
from students.models import Student

# 测试用户登录和权限控制
def test_permissions():
    # 创建测试客户端
    client = Client()
    
    print("=== 测试权限控制 ===")
    
    # 测试1: 学生用户(001)登录
    print("\n1. 测试学生用户(001)登录:")
    login_success = client.login(username='001', password='123456')
    print(f"   登录结果: {'成功' if login_success else '失败'}")
    
    if login_success:
        # 测试学生可以访问个人中心
        response = client.get('/profile/')
        print(f"   访问个人中心: {'允许' if response.status_code == 200 else '拒绝'}")
        
        # 测试学生可以访问成绩查询
        response = client.get('/my-scores/')
        print(f"   访问成绩查询: {'允许' if response.status_code == 200 else '拒绝'}")
        
        # 测试学生无法访问学生列表(管理页面)
        response = client.get('/students/')
        print(f"   访问学生列表(管理页面): {'拒绝' if response.status_code in [302, 403] else '允许(错误!)'}")
        
        # 测试学生无法访问课程管理
        response = client.get('/courses/')
        print(f"   访问课程管理: {'拒绝' if response.status_code in [302, 403] else '允许(错误!)'}")
        
        # 测试学生无法访问成绩管理
        response = client.get('/scores/')
        print(f"   访问成绩管理: {'拒绝' if response.status_code in [302, 403] else '允许(错误!)'}")
        
        # 测试学生无法访问班级管理
        response = client.get('/classes/')
        print(f"   访问班级管理: {'拒绝' if response.status_code in [302, 403] else '允许(错误!)'}")
        
        # 测试学生无法访问院系管理
        response = client.get('/departments/')
        print(f"   访问院系管理: {'拒绝' if response.status_code in [302, 403] else '允许(错误!)'}")
        
        # 测试学生无法访问教师管理
        response = client.get('/teachers/')
        print(f"   访问教师管理: {'拒绝' if response.status_code in [302, 403] else '允许(错误!)'}")
        
        # 退出登录
        client.logout()
    
    # 测试2: 管理员用户(admin)登录
    print("\n2. 测试管理员用户(admin)登录:")
    login_success = client.login(username='admin', password='admin123')
    print(f"   登录结果: {'成功' if login_success else '失败'}")
    
    if login_success:
        # 测试管理员可以访问学生列表
        response = client.get('/students/')
        print(f"   访问学生列表: {'允许' if response.status_code == 200 else '拒绝(错误!)'}")
        
        # 测试管理员可以访问课程管理
        response = client.get('/courses/')
        print(f"   访问课程管理: {'允许' if response.status_code == 200 else '拒绝(错误!)'}")
        
        # 测试管理员可以访问成绩管理
        response = client.get('/scores/')
        print(f"   访问成绩管理: {'允许' if response.status_code == 200 else '拒绝(错误!)'}")
        
        # 退出登录
        client.logout()
    
    print("\n=== 测试完成 ===")

if __name__ == '__main__':
    test_permissions()
