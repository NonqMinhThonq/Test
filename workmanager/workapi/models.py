from django.db import models
from django.contrib.auth.models import User

class WorkBoard(models.Model):
    name = models.CharField(max_length=100)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        ordering = ['id'] 

class TaskList(models.Model):
    name = models.CharField(max_length=100)
    board = models.ForeignKey(WorkBoard, related_name='tasklists', on_delete=models.CASCADE)

class Task(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=[('Pending', 'Pending'), ('Completed', 'Completed')])
    list = models.ForeignKey(TaskList, related_name='tasks', on_delete=models.CASCADE)
    assigned_to = models.ForeignKey(User, related_name='tasks', on_delete=models.SET_NULL, null=True)
    due_date = models.DateField(null=True, blank=True)
    is_deleted = models.BooleanField(default=False, null=True)

class Comment(models.Model):
    task = models.ForeignKey(Task, related_name='comments', on_delete=models.CASCADE)
    content = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

class Attachment(models.Model):
    task = models.ForeignKey(Task, related_name='attachments', on_delete=models.CASCADE)
    file = models.FileField(upload_to='attachments/')
