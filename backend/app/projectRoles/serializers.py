from rest_framework import serializers
from app.projectRoles.models import ProjectRole


class ProjectRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectRole
        fields = ['id', 'role', 'created', 'updated']