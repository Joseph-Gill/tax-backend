from rest_framework import serializers
from app.tasks.models import Task
from app.userProfiles.serializers import UserProfileSerializer


class TaskSerializer(serializers.ModelSerializer):
    assigned_user = UserProfileSerializer(
        required=False
    )

    class Meta:
        model = Task
        fields = ['id', 'planned_completion_date', 'due_date', 'title', 'description', 'documents', 'created', 'updated', 'assigned_user']
