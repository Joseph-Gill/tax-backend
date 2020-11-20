from django.db import models


class TaxConsequence(models.Model):
    location: models.CharField(
        max_length=150
    )

    # This will store different Tax Types ( i.e. Corporate Income Tax, Withholding Tax, etc )
    # This will be stored in a drop down
    # Looking to use this information at a later date to possibly generate Tax Rulings
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
