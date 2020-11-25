from rest_framework import serializers
from app.organizations.models import Organization
from app.userProfiles.serializers import UserProfileSerializer


class OrganizationSerializer(serializers.ModelSerializer):
    user_profiles = UserProfileSerializer(
        required=False,
        many=True
    )

    class Meta:
        model = Organization
        fields = ['name', 'created', 'updated', 'group', 'user_profiles']