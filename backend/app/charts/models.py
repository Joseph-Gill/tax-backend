from django.db import models
from app.steps.models import Step


class Chart(models.Model):
    # This needs to store an Array of Objects, possibly JSON??
    clinks = models.TextField(
        blank=True
    )

    # This needs to store an Array of Objects, possibly JSON??
    slinks = models.TextField(
        blank=True
    )

    # This needs to store an Array of Objects, possibly JSON??
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
