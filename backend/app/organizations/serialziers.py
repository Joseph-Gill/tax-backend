from rest_framework import serializers
from app.organizations.models import Organization
from app.userProfiles.models import UserProfile
from app.users.serializers import UserSerializer


class UserProfileOrganizationSerializer(serializers.ModelSerializer):
    user = UserSerializer(
        required=False
    )

    class Meta:
        model = UserProfile
        fields = ['user']


class OrganizationSerializer(serializers.ModelSerializer):
    user_profiles = UserProfileOrganizationSerializer(
        required=False,
        many=True
    )

    class Meta:
        model = Organization
        fields = ['id', 'name', 'created', 'updated', 'group', 'user_profiles']
