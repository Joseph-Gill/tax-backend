from rest_framework import serializers
from app.taskDocuments.serializers import TaskDocumentSerializer
from app.tasks.models import Task
from app.userProfiles.serializers import UserProfileSerializer


class TaskSerializer(serializers.ModelSerializer):
    assigned_user = UserProfileSerializer(
        required=False
    )

    task_documents = TaskDocumentSerializer(
        required=False,
        many=True
    )

    class Meta:
        model = Task
        fields = ['id', 'planned_completion_date', 'due_date', 'title', 'description', 'task_documents', 'created', 'updated', 'assigned_user']
