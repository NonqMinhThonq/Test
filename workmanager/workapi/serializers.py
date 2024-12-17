from rest_framework import serializers
from .models import WorkBoard, TaskList, Task, Comment, Attachment

class WorkBoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkBoard
        fields = '__all__'

class TaskListSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskList
        fields = '__all__'

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'
        
class TaskStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['status']

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'

class AttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attachment
        fields = '__all__'
