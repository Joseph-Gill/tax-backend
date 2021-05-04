from rest_framework import serializers
from app.entityHistories.models import EntityHistory


class EntityHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = EntityHistory
        fields = ['id', 'entity', 'chart', 'action']
