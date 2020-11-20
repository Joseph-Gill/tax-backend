from django.db import models

from app.projectRoles.models import ProjectRole
from app.steps.models import Step


class Project(models.Model):
    name = models.CharField(
        max_length=150
    )

    description = models.TextField(
        blank=True
    )

    start_date = models.DateField()

    end_date = models.DateField()

    status = models.CharField(
        max_length=30
    )

    created = models.DateTimeField(
        auto_now_add=True
    )

    updated = models.DateTimeField(
        auto_now=True
    )

    steps = models.ForeignKey(
        to=Step,
        on_delete=models.CASCADE,
        related_name='project',
        null=True,
        blank=True
    )

    assigned_users_roles = models.ForeignKey(
        to=ProjectRole,
        on_delete=models.CASCADE,
        related_name='project',
        null=True,
        blank=True
    )

    def __str__(self):
        return f'Project #{self.pk} for Group #{self.group.id} - Name: {self.project.group.name}'
