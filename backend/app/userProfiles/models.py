from django.db import models
from django.dispatch import receiver
from django.conf import settings

from app.groups.models import Group
from app.organizations.models import Organization
from app.projectRoles.models import ProjectRole
from app.registration.signals import post_user_registration_validation
from app.tasks.models import Task


class UserProfile(models.Model):
    phone_number = models.CharField(
        max_length=13,
        blank=True
    )

    created = models.DateTimeField(
        auto_now_add=True,
    )

    updated = models.DateTimeField(
        auto_now=True
    )

    organizations = models.ManyToManyField(
        to=Organization,
        related_name='user_profiles'
    )

    user = models.OneToOneField(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='user_profile',
        blank=True,
        null=True
    )

    groups = models.ManyToManyField(
        to=Group,
        related_name='users'
    )

    assigned_project_roles = models.ForeignKey(
        to=ProjectRole,
        on_delete=models.CASCADE,
        related_name='user',
        blank=True,
        null=True
    )

    assigned_tasks = models.ForeignKey(
        to=Task,
        on_delete=models.SET_NULL,
        related_name='assigned_user',
        blank=True,
        null=True
    )

    def __str__(self):
        return f'User Profile #{self.pk} for {self.registration_profile.user.email}'


@receiver(post_user_registration_validation)
def create_user_profile(sender, user, **kwargs):
    UserProfile(user=user).save()
