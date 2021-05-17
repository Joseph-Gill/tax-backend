from rest_framework import serializers
from app.charts.models import Chart
from app.projects.models import Project
from app.steps.models import Step


class ChartProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'name']


class ChartStepSerializer(serializers.ModelSerializer):
    project = ChartProjectSerializer(
        required=False
    )

    class Meta:
        model = Step
        fields = ['id', 'effective_date', 'number', 'project']


class ChartSerializer(serializers.ModelSerializer):
    step = ChartStepSerializer(
        required=False
    )

    class Meta:
        model = Chart
        fields = ['id', 'clinks', 'slinks', 'nodes', 'created', 'updated', 'step']
