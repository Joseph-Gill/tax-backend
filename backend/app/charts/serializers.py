from rest_framework import serializers
from app.charts.models import Chart
from app.steps.models import Step


class ChartStepSerializer(serializers.ModelSerializer):
    class Meta:
        model = Step
        fields = ['id', 'effective_date']


class ChartSerializer(serializers.ModelSerializer):
    step = ChartStepSerializer(
        required=False
    )

    class Meta:
        model = Chart
        fields = ['id', 'clinks', 'slinks', 'nodes', 'created', 'updated', 'step']
