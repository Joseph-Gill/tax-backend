from rest_framework import serializers
from app.projectRoles.models import ProjectRole
from app.projects.models import Project


class ProjectProjectRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'group', 'name']


class ProjectRoleSerializer(serializers.ModelSerializer):
    project = ProjectProjectRoleSerializer(
        required=False
    )

    class Meta:
        model = ProjectRole
        fields = ['id', 'role', 'created', 'updated', 'project']