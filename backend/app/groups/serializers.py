from rest_framework import serializers

from app.groups.models import Group
from app.userProfiles.models import UserProfile


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['id', 'name', 'avatar', 'created', 'updated', 'entities', 'projects', 'organizations', 'users']
        # optional_fields = ['user']
