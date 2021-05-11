from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from rest_framework import serializers
from app.groups.models import Group
from app.organizations.serialziers import OrganizationSerializer
from app.projectRoles.serializers import ProjectRoleSerializer
from app.projects.models import Project
from app.registration.serializers import email_does_not_exist
from app.tasks.models import Task
from app.userProfiles.models import UserProfile
from app.users.serializers import UserSerializer

User = get_user_model()


# Used by UserProfileSerializer to prevent circular serialization from Project Serializer
class ProfileProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'name']


# Used by UserProfileSerializer to prevent circular serialization from Group Serializer
class ProfileGroupSerializer(serializers.ModelSerializer):
    projects = ProfileProjectSerializer(
        required=False,
        many=True
    )

    class Meta:
        model = Group
        fields = ['id', 'name', 'projects', 'users', 'avatar']


# Used by UserProfileSerializer to prevent circular serialization from Task Serializer
class ProfileTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'planned_completion_date', 'due_date']


class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(
        required=False
    )

    organizations = OrganizationSerializer(
        required=False,
        many=True
    )

    groups = ProfileGroupSerializer(
        required=False,
        many=True
    )

    assigned_project_roles = ProjectRoleSerializer(
        required=False,
        many=True
    )

    assigned_tasks = ProfileTaskSerializer(
        required=False,
        many=True
    )

    favorite_groups = ProfileGroupSerializer(
        required=False,
        many=True
    )

    class Meta:
        model = UserProfile
        fields = ['id', 'phone_number', 'country', 'user', 'created', 'updated', 'organizations', 'groups', 'favorite_groups', 'assigned_project_roles', 'assigned_tasks']


class UpdateUserProfileSerializer(serializers.Serializer):
    email = serializers.EmailField(label='E-Mail Address', validators=[email_does_not_exist], required=False)
    password = serializers.CharField(label='password', write_only=True, allow_blank=True)
    password_repeat = serializers.CharField(label='password_repeat', write_only=True, allow_blank=True)
    first_name = serializers.CharField(label='First name', required=False)
    last_name = serializers.CharField(label='Last name', required=False)
    phone_number = serializers.CharField(label='phone number', required=False, allow_null=True)
    country = serializers.CharField(label='country', required=False, allow_null=True)

    def validate(self, data):
        if data.get('password') != data.get('password_repeat'):
            raise ValidationError(message='Passwords do not match!')
        return data

    def save(self, validated_data, user_profile):
        if validated_data.get('password'):
            user_profile.user.set_password(validated_data.get('password'))
        user_profile.phone_number = validated_data.get('phone_number')
        user_profile.country = validated_data.get('country')
        if validated_data.get('email'):
            user_profile.user.email = validated_data.get('email')
            user_profile.user.username = validated_data.get('email')
        user_profile.user.first_name = validated_data.get('first_name')
        user_profile.user.last_name = validated_data.get('last_name')
        user_profile.save()
        user_profile.user.save()
        return user_profile
