from rest_framework import serializers
from app.entities.models import Entity


class EntitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Entity
        fields = ['id', 'pid', 'name', 'legal_form', 'location', 'tax_rate', 'created', 'updated']
