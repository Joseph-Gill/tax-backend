from django.db import models
from app.charts.models import Chart
from app.entities.models import Entity
from app.userProfiles.models import UserProfile


class EntityHistory(models.Model):
    # stores the key word of what action occurred to the related entity during the step
    action = models.CharField(
        max_length=200
    )

    created = models.DateTimeField(
        auto_now_add=True
    )

    updated = models.DateTimeField(
        auto_now=True
    )

    # Used to track official histories of an entity to show on the Entity History timeline.
    # Changes made by GroupAdd / GroupEdit are pending false, changes made in a StepChart
    # default to true. Once a step / project is completed, all the relevant histories are
    # change to pending false, becoming official histories
    pending = models.BooleanField(
        default=False
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
        related_name='chart_histories',
        blank=True,
        null=True
    )

    creator = models.ForeignKey(
        to=UserProfile,
        on_delete=models.SET_NULL,
        related_name='entity_actions',
        blank=True,
        null=True
    )

    creating_action = models.ForeignKey(
        to='EntityHistory',
        on_delete=models.CASCADE,
        related_name='affected_entities',
        blank=True,
        null=True
    )

    def __str__(self):
        return f'Entity Log #{self.id} for {self.entity.name}'
