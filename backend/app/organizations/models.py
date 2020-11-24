from django.db import models

from app.groups.models import Group


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
