from rest_framework import serializers
from app.charts.models import Chart


class ChartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chart
        fields = ['id', 'clinks', 'slinks', 'nodes', 'created', 'updated']
