from django.db import models

from app.steps.models import Step
from app.userProfiles.models import UserProfile


class Task(models.Model):
    planned_completion_date = models.DateField()

    due_date = models.DateField()

    title = models.CharField(
        max_length=150
    )

    description = models.TextField()

    status = models.CharField(
        max_length=15,
        default='Not Started'
    )

    created = models.DateTimeField(
        auto_now_add=True
    )

    updated = models.DateTimeField(
        auto_now=True
    )

    step = models.ForeignKey(
        to=Step,
        on_delete=models.CASCADE,
        related_name='tasks',
        null=True,
        blank=True
    )

    assigned_user = models.ForeignKey(
        to=UserProfile,
        on_delete=models.SET_NULL,
        related_name='assigned_tasks',
        blank=True,
        null=True
    )

    def __str__(self):
        return f'Task #{self.pk} for Project #{self.step.project.id}, Step #{self.step.number}'
