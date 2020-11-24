from django.db import models

class Group(models.Model):
    name = models.CharField(
        max_length=150
    )

    created = models.DateTimeField(
        auto_now_add=True
    )

    updated = models.DateTimeField(
        auto_now=True
    )

    avatar = models.ImageField(
        blank=True,
        null=True
    )

    def __str__(self):
        return f'Group #{self.pk} - Name: {self.name}'
