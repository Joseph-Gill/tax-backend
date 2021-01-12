from django.contrib.auth import get_user_model
from rest_framework import serializers
from app.userProfiles.models import UserProfile

User = get_user_model()


class UserUserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['id', 'country', 'phone_number']


class UserSerializer(serializers.ModelSerializer):
    user_profile = UserUserProfileSerializer(
        required=False
    )

    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'username', 'user_profile']
        read_only_fields = ['email']


class UpdateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'username']
