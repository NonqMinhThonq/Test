import os
import django
import random
from datetime import date, timedelta

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "workmanager.settings")
django.setup()

from django.contrib.auth.models import User
from workapi.models import WorkBoard, TaskList, Task, Comment, Attachment

# Tạo người dùng
user1 = User.objects.create_user(username='user1@test.com', password='123456')
user2 = User.objects.create_user(username='user2@test.com', password='123456')
users = [user1, user2]

# Tạo bảng công việc
workboard1 = WorkBoard.objects.create(name='Dự án A', created_by=user1)
workboard2 = WorkBoard.objects.create(name='Dự án B', created_by=user2)
workboards = [workboard1, workboard2]

# Tạo danh sách công việc
tasklist1 = TaskList.objects.create(name='Danh sách 1', board=workboard1)
tasklist2 = TaskList.objects.create(name='Danh sách 2', board=workboard2)
tasklists = [tasklist1, tasklist2]

# Tạo thẻ công việc
statuses = ['Pending', 'Completed']
for i in range(10):
    task = Task.objects.create(
        name=f'Task {i+1}',
        description=f'Mô tả công việc {i+1}',
        status=random.choice(statuses),
        list=random.choice(tasklists),
        assigned_to=random.choice(users),
        due_date=date.today() + timedelta(days=random.randint(1, 30))
    )

# Tạo bình luận và đính kèm file
tasks = Task.objects.all()
for task in tasks:
    Comment.objects.create(task=task, content=f'Bình luận cho {task.name}', created_by=random.choice(users))
    Attachment.objects.create(task=task, file='path/to/file', )

print("Đã thêm dữ liệu ảo vào cơ sở dữ liệu.")
