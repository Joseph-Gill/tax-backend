from django.db import models


class Entity(models.Model):
    # Stores the parent Id number of an entity, can have no pid making it the top most entity on a chart
    pid = models.CharField(
        max_length=150,
        null=True,
        blank=True
    )

    name = models.CharField(
        max_length=150
    )

    # Can an Entity not have a Legal Form??
    legal_form = models.CharField(
        max_length=150,
        null=True,
        blank=True
    )

    # Can an Entity not have a location??
    location = models.CharField(
        max_length=150,
        null=True,
        blank=True
    )

    # Possibly a decimal number?? / Can an Entity not have a tax rate??
    tax_rate = models.IntegerField()

    created = models.DateTimeField(
        auto_now_add=True
    )

    updated = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return f'Entity #{self.pk}'
