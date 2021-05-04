from django.db import models
from app.charts.models import Chart
from app.entities.models import Entity


class EntityHistory(models.Model):
    action = models.CharField(
        max_length=30
    )

    # used to store the temporary id used in frontend before an entity
    # is officially created by completing a step/project
    temp_id = models.IntegerField(
        blank=True,
        null=True
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
        related_name='entity_histories',
        blank=True,
        null=True
    )

    chart = models.ForeignKey(
        to=Chart,
        on_delete=models.CASCADE,
        related_name='chart_histories'
    )

    def __str__(self):
        return f'Entity Log #{self.id} for {self.entity.name} and Chart #{self.chart.id}'
