from django.db import models


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

    def __str__(self):
        return f'Organization #{self.pk} - Name: {self.name} for Group: {self.group.name}'
