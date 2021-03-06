from rest_framework import serializers
from app.charts.serializers import ChartSerializer
from app.entities.serializers import EntitySerializer
from app.entityHistories.models import EntityHistory


class AffectedEntitiesSerializer(serializers.ModelSerializer):
    entity = EntitySerializer(
        required=False
    )

    class Meta:
        model = EntityHistory
        fields = ['id', 'entity', 'action']


class EntityHistoryHistorySerializer(serializers.ModelSerializer):
    entity = EntitySerializer(
        required=False
    )

    affected_entities = AffectedEntitiesSerializer(
        required=False,
        many=True
    )

    class Meta:
        model = EntityHistory
        fields = ['id', 'entity', 'action', 'affected_entities']


class EntityHistorySerializer(serializers.ModelSerializer):
    entity = EntitySerializer(
        required=False
    )

    chart = ChartSerializer(
        required=False
    )

    affected_entities = EntityHistoryHistorySerializer(
        required=False,
        many=True
    )

    creating_action = EntityHistoryHistorySerializer(
        required=False
    )

    class Meta:
        model = EntityHistory
        fields = ['id', 'entity', 'chart', 'action', 'changed_legal_form', 'affected_entities', 'creator', 'pending', 'creating_action', 'created']
