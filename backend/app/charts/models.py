from django.db import models


class Chart(models.Model):
    # This needs to store an Array of Objects, possibly JSON??
    clinks = models.TextField(
        blank=True
    )

    # This needs to store an Array of Objects, possibly JSON??
    slinks = models.TextField(
        blank=True
    )

    # This needs to store an Array of Objects, possibly JSON??
    nodes = models.TextField()

    created = models.DateTimeField(
        auto_now_add=True
    )

    updated = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return f'Chart #{self.pk} for Project #{self.step.project}, Step #{self.step.number}'
