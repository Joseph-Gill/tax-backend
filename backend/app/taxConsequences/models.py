from django.db import models


class TaxConsequence(models.Model):
    location: models.CharField(
        max_length=150
    )

    # Unsure what type is storing at this time, discuss with Alain
    type: models.CharField(
        max_length=150
    )

    description: models.TextField()

    created = models.DateTimeField(
        auto_now_add=True
    )

    updated = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return f'Tax Consequence #{self.pk} for Project #{self.step.project.id}, Step #{self.step.number}'
