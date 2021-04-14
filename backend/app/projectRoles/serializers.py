from django.contrib.auth import get_user_model
from rest_framework import serializers
from app.projectRoles.models import ProjectRole
from app.projects.models import Project
from app.userProfiles.models import UserProfile

User = get_user_model()


class ProjectProjectRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'group', 'name']


class UserProfileProjectRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['id', 'country']


class ProjectRoleSerializer(serializers.ModelSerializer):
    project = ProjectProjectRoleSerializer(
        required=False
    )

    user = UserProfileProjectRoleSerializer(
        required=False
    )

    class Meta:
        model = ProjectRole
        fields = ['id', 'role', 'created', 'updated', 'project', 'user']
