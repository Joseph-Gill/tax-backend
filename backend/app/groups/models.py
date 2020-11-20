from django.db import models

from app.entities.models import Entity
from app.projects.models import Project


class Group(models.Model):
    name = models.CharField(
        max_length=150
    )

    created = models.DateTimeField(
        auto_now_add=True
    )

    updated = models.DateTimeField(
        auto_now=True
    )

    entities = models.ForeignKey(
        to=Entity,
        on_delete=models.CASCADE,
        related_name='group',
        null=True,
        blank=True
    )

    projects = models.ForeignKey(
        to=Project,
        on_delete=models.CASCADE,
        related_name='group',
        null=True,
        blank=True
    )

    def __str__(self):
        return f'Group #{self.pk} - Name: {self.name}'
