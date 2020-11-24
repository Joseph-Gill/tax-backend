from django.db import models

from app.projects.models import Project
from app.userProfiles.models import UserProfile


class ProjectRole(models.Model):
    # Role choices are Core, Legal, Tax, Other
    role = models.CharField(
        max_length=10
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
        related_name='assigned_users_roles',
        null=True,
        blank=True
    )

    user = models.ForeignKey(
        to=UserProfile,
        on_delete=models.CASCADE,
        related_name='assigned_project_roles',
        blank=True,
        null=True
    )

    def __str__(self):
        return f'Project Role #{self.pk} for User - {self.registration_profile.user.email}'
