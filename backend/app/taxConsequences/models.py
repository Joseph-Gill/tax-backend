from django.db import models
from app.steps.models import Step
from app.userProfiles.models import UserProfile


class TaxConsequence(models.Model):
    location = models.CharField(
        max_length=150,
    )

    # This will store different Tax Types ( i.e. Corporate Income Tax, Withholding Tax, etc )
    # This will be stored in a drop down
    # Looking to use this information at a later date to possibly generate Tax Rulings
    type = models.CharField(
        max_length=150,
        null=True,
        blank=True
    )

    # The three Tax Consequence "statuses" depend on the state of description and reviewed
    # 1) Open - description is blank ( i.e. false ) and reviewed is false
    # 2) To Review - description is filled in ( i.e. true ) and reviewed is false
    # 3) Reviewed - description is filled in (i.e. true ) and reviewed is true
    description = models.TextField(
        blank=True,
        null=True
    )

    reviewed = models.BooleanField(
        default=False
    )

    created = models.DateTimeField(
        auto_now_add=True
    )

    updated = models.DateTimeField(
        auto_now=True
    )

    step = models.ForeignKey(
        to=Step,
        on_delete=models.CASCADE,
        related_name='tax_consequences',
        null=True,
        blank=True
    )

    reviewing_user = models.ForeignKey(
        to=UserProfile,
        on_delete=models.SET_NULL,
        related_name='reviewed_tax_consequences',
        null=True,
        blank=True
    )

    creating_user = models.ForeignKey(
        to=UserProfile,
        on_delete=models.SET_NULL,
        related_name='created_tax_consequences',
        null=True,
        blank=True
    )

    def __str__(self):
        return f'Tax Consequence #{self.pk} for Project #{self.step.project.id}, Step #{self.step.number}'
