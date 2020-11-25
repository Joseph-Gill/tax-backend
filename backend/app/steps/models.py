from django.db import models
from app.projects.models import Project


class Step(models.Model):
    number = models.IntegerField(
        blank=True,
        null=True
    )

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

    project = models.ForeignKey(
        to=Project,
        on_delete=models.CASCADE,
        related_name='steps',
        null=True,
        blank=True
    )

    def __str__(self):
        return f'Step #{self.number} (id #{self.id}) for Project: {self.project.name} - Group: {self.project.group.name}'
