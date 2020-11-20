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

    groups = models.ManyToManyField(
        to=Group,
        related_name='organizations'
    )

    def __str__(self):
        return f'Organization #{self.pk} - Name: {self.name}'
