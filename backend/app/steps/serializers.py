from rest_framework import serializers
from app.charts.serializers import ChartSerializer
from app.steps.models import Step
from app.tasks.serializers import TaskSerializer
from app.taxConsequences.serializers import TaxConsequenceSerializer


class StepSerializer(serializers.ModelSerializer):
    chart = ChartSerializer(
        required=False
    )

    tax_consequences = TaxConsequenceSerializer(
        required=False,
        many=True
    )

    tasks = TaskSerializer(
        required=False,
        many=True
    )

    class Meta:
        model = Step
        fields = ['id', 'number', 'description', 'effective_date', 'status', 'created', 'updated', 'chart', 'tax_consequences', 'tasks']
