from rest_framework import serializers
from app.steps.models import Step


class StepSerializer(serializers.ModelSerializer):
    class Meta:
        model = Step
        fields = ['id', 'number', 'description', 'effective_date', 'status', 'created', 'updated', 'chart', 'tax_consequences', 'tasks']
