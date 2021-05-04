from django.db import models
from app.entities.models import Entity


class Sharehold(models.Model):
    percent_ownership = models.DecimalField(
        max_digits=5,
        decimal_places=4,
        blank=True,
        null=True
    )

    created = models.DateTimeField(
        auto_now_add=True
    )

    updated = models.DateTimeField(
        auto_now=True
    )

    parent = models.ForeignKey(
        to=Entity,
        on_delete=models.CASCADE,
        related_name='shareholds_parent'
    )

    child = models.ForeignKey(
        to=Entity,
        on_delete=models.CASCADE,
        related_name='shareholds_child'
    )

    def __str__(self):
        return f'Sharehold #{self.id} between {self.parent.name} and {self.child.name}'
