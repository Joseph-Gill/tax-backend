from rest_framework import serializers
from app.projects.models import Project
from app.steps.serializers import StepSerializer


class ProjectSerializer(serializers.ModelSerializer):
    steps = StepSerializer(
        required=False,
        many=True
    )

    class Meta:
        model = Project
        fields = ['id', 'name', 'description', 'start_date', 'end_date', 'status', 'created', 'updated', 'steps']
