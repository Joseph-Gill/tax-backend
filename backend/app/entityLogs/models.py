from django.db import models
from app.charts.models import Chart
from app.entities.models import Entity


class EntityLog(models.Model):
    action = models.CharField(
        max_length=30
    )

    created = models.DateTimeField(
        auto_now_add=True
    )

    updated = models.DateTimeField(
        auto_now=True
    )

    entity = models.ForeignKey(
        to=Entity,
        on_delete=models.CASCADE,
        related_name='entity_logs'
    )

    chart = models.ForeignKey(
        to=Chart,
        on_delete=models.CASCADE,
        related_name='chart_logs'
    )

    def __str__(self):
        return f'Entity Log #{self.id} for {self.entity.name} and Chart #{self.chart.id}'
