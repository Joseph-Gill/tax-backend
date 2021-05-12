from rest_framework import serializers
from app.charts.serializers import ChartSerializer
from app.entities.serializers import EntitySerializer
from app.entityHistories.models import EntityHistory


class EntityHistorySerializer(serializers.ModelSerializer):
    entity = EntitySerializer(
        required=False
    )

    affected_entities = EntitySerializer(
        required=False,
        many=True
    )

    chart = ChartSerializer(
        required=False
    )

    class Meta:
        model = EntityHistory
        fields = ['id', 'entity', 'chart', 'action', 'affected_entities', 'creator', 'pending']
