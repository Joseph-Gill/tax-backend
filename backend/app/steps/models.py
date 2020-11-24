from django.db import models

from app.charts.models import Chart
from app.projects.models import Project


class Step(models.Model):
    description = models.TextField()

    effective_date = models.DateField()

    # There are only 3 current statuses - Not Started, Ongoing, and Completed
    status = models.CharField(
        max_length=30
    )

    created = models.DateTimeField(
        auto_now_add=True
    )

    updated = models.DateTimeField(
        auto_now=True
    )

    chart = models.OneToOneField(
        to=Chart,
        on_delete=models.CASCADE,
        related_name='step',
        null=True,
        blank=True
    )

    project = models.ForeignKey(
        to=Project,
        on_delete=models.CASCADE,
        related_name='steps',
        null=True,
        blank=True
    )

    def __str__(self):
        return f'Step #{self.number} for Project #{self.project.id}'
