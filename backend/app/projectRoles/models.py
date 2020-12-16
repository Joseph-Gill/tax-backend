from django.db import models
from django.dispatch import receiver
from app.projects.models import Project
from app.projects.signals import post_user_project_creation
from app.userProfiles.models import UserProfile


class ProjectRole(models.Model):
    # Role choices are core, legal, tax, other, coreLegal, or coreTax
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
        return f'Project Role #{self.pk} for User - {self.user.user.email}'


@receiver(post_user_project_creation)
def create_user_profile(user_profile, new_project, **kwargs):
    new_project_role = ProjectRole(
        role="Core",
        user=user_profile
    )
    new_project_role.save()
    new_project.assigned_users_roles.add(new_project_role)
