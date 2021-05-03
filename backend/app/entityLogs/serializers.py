from rest_framework import serializers
from app.entityLogs.models import EntityLog


class EntityLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = EntityLog
        fields = ['id', 'entity', 'chart', 'action']
