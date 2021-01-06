from rest_framework import serializers

from app.projectRoles.serializers import ProjectRoleSerializer
from app.steps.models import Step
from app.taskDocuments.serializers import TaskDocumentSerializer
from app.tasks.models import Task
from app.userProfiles.models import UserProfile
from app.users.serializers import UserSerializer


class TaskStepSerializer(serializers.ModelSerializer):
    class Meta:
        model = Step
        fields = ['id', 'number']


class TaskUserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(
        required=False
    )

    assigned_project_roles = ProjectRoleSerializer(
        required=False,
        many=True
    )

    class Meta:
        model = UserProfile
        fields = ['id', 'country', 'user', 'assigned_project_roles']


class TaskSerializer(serializers.ModelSerializer):
    assigned_user = TaskUserProfileSerializer(
        required=False
    )

    task_documents = TaskDocumentSerializer(
        required=False,
        many=True
    )

    step = TaskStepSerializer(
        required=False
    )

    class Meta:
        model = Task
        fields = ['id', 'planned_completion_date', 'due_date', 'title', 'description', 'task_documents', 'created', 'updated', 'assigned_user', 'step', 'status']
