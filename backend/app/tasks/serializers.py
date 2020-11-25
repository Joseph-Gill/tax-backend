from rest_framework import serializers
from app.tasks.models import Task


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'planned_completion_date', 'due_date', 'title', 'description', 'documents', 'created', 'updated', 'assigned_user']
