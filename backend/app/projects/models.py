from django.db import models
from app.groups.models import Group


class Project(models.Model):
    name = models.CharField(
        max_length=150
    )

    description = models.TextField(
        blank=True
    )

    start_date = models.DateField(
        blank=True,
        null=True
    )

    end_date = models.DateField(
        blank=True,
        null=True
    )

    # Ongoing - Not Started, Completed, Not Implemented
    status = models.CharField(
        max_length=30
    )

    created = models.DateTimeField(
        auto_now_add=True
    )

    updated = models.DateTimeField(
        auto_now=True
    )

    group = models.ForeignKey(
        to=Group,
        on_delete=models.CASCADE,
        related_name='projects',
        null=True,
        blank=True
    )

    def __str__(self):
        return f'Project #{self.pk} for Group #{self.group.id} - Name: {self.group.name}'
