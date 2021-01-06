from django.db import models
from app.tasks.models import Task


class TaskDocument(models.Model):
    created = models.DateTimeField(
        auto_now_add=True
    )

    updated = models.DateTimeField(
        auto_now=True
    )

    name = models.CharField(
        max_length=500,
        blank=True,
        null=True
    )

    document = models.FileField(
        blank=True,
        null=True
    )

    task = models.ForeignKey(
        to=Task,
        on_delete=models.CASCADE,
        related_name='task_documents',
        null=True,
        blank=True
    )
