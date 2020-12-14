from rest_framework import serializers

from app.entities.serializers import EntitySerializer
from app.groups.models import Group
from app.organizations.serialziers import OrganizationSerializer
from app.projects.serializers import ProjectSerializer
from app.registration.models import RegistrationProfile
from app.userProfiles.serializers import UserProfileSerializer
from app.users.serializers import UserSerializer


class GroupRegistrationSerializer(serializers.ModelSerializer):
    user = UserSerializer(
        required=False
    )

    class Meta:
        model = RegistrationProfile
        fields = ['user', 'code_used']


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

    invited_new_users = GroupRegistrationSerializer(
        required=False,
        many=True
    )

    class Meta:
        model = Group
        fields = ['id', 'name', 'avatar', 'created', 'updated', 'entities', 'projects', 'organizations', 'users', 'invited_new_users']
