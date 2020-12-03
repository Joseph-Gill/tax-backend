from rest_framework import serializers
from app.organizations.models import Organization


class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = ['name', 'created', 'updated', 'group']
