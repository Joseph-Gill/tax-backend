from django.db import models
from django.dispatch import receiver

from app.groups.models import Group
from app.groups.signals import post_user_group_creation


class Organization(models.Model):
    name = models.CharField(
        max_length=150
    )

    created = models.DateTimeField(
        auto_now_add=True
    )

    updated = models.DateTimeField(
        auto_now=True
    )

    group = models.ForeignKey(
        to=Group,
        on_delete=models.CASCADE,
        related_name='organizations',
        null=True,
        blank=True
    )

    def __str__(self):
        return f'Organization #{self.pk} - Name: {self.name} for Group: {self.group.name}'


@receiver(post_user_group_creation)
def create_user_profile(user_profile, name, new_group, **kwargs):
    new_organization = Organization(
        name=name,
        group=new_group
    )
    new_organization.save()
    new_organization.user_profiles.add(user_profile)
