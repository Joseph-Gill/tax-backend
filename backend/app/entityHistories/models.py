from django.db import models
from app.charts.models import Chart
from app.entities.models import Entity


class EntityHistory(models.Model):
    # stores the key word of what action occurred to the related entity during the step
    action = models.CharField(
        max_length=30
    )

    # This is used to store the JSON data for other entities affected by this action
    affected_entities = models.TextField(
        blank=True
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
        on_delete=models.SET_NULL,
        related_name='chart_histories',
        blank=True,
        null=True
    )

    def __str__(self):
        return f'Entity Log #{self.id} for {self.entity.name}'
