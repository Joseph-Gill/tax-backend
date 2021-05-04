from django.db import models
from app.steps.models import Step


class Chart(models.Model):
    # This is used to store the JSON data for the chart's CLinks
    clinks = models.TextField(
        blank=True
    )

    # This is used to store the JSON data for the chart's SLinks
    slinks = models.TextField(
        blank=True
    )

    # # This is used to store the JSON data for the chart's Nodes
    nodes = models.TextField()

    created = models.DateTimeField(
        auto_now_add=True
    )

    updated = models.DateTimeField(
        auto_now=True
    )

    step = models.OneToOneField(
        to=Step,
        on_delete=models.CASCADE,
        related_name='chart',
        null=True,
        blank=True
    )

    def __str__(self):
        return f'Chart #{self.pk} for Group - Name: {self.step.project.group.name} - Project #{self.step.project.id}, Step #{self.step.number}'
