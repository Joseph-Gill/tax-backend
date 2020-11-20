from django.db import models


class Task(models.Model):
    planned_completion_date = models.DateField()

    due_date = models.DateField()

    description = models.TextField()

    documents = models.FileField(
        blank=True,
        null=True
    )

    created = models.DateTimeField(
        auto_now_add=True
    )

    updated = models.DateField(
        auto_now=True
    )

    def __str__(self):
        return f'Task #{self.pk} for Project #{self.step.project.id}, Step #{self.step.number}'
