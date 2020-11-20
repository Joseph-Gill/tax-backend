from django.db import models


class Chart(models.Model):
    # This needs to store an Array of Objects, possibly JSON??
    clinks = models.CharField(
        null=True,
        blank=True
    )

    # This needs to store an Array of Objects, possibly JSON??
    slinks = models.CharField(
        null=True,
        blank=True
    )

    # This needs to store an Array of Objects, possibly JSON??
    nodes = models.CharField(
        null=True,
        blank=True
    )

    created = models.DateTimeField(
        auto_now_add=True
    )

    updated = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return f'Chart #{self.pk}'
