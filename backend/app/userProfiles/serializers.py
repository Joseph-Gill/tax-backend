from rest_framework import serializers
from app.userProfiles.models import UserProfile
from app.users.serializers import UserSerializer


class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(
        required=False
    )

    class Meta:
        model = UserProfile
        fields = ['id', 'phone_number', 'user', 'created', 'updated']