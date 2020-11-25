from rest_framework import serializers

from app.entities.serializers import EntitySerializer
from app.groups.models import Group
from app.organizations.serialziers import OrganizationSerializer
from app.projects.serializers import ProjectSerializer
from app.userProfiles.serializers import UserProfileSerializer


class GroupSerializer(serializers.ModelSerializer):
    users = UserProfileSerializer(
        required=False,
        many=True
    )

    entities = EntitySerializer(
        required=False,
        many=True
    )

    projects = ProjectSerializer(
        required=False,
        many=True
    )

    organizations = OrganizationSerializer(
        required=False,
        many=True
    )

    class Meta:
        model = Group
        fields = ['id', 'name', 'avatar', 'created', 'updated', 'entities', 'projects', 'organizations', 'users']
