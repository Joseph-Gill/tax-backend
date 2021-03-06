from django.db import models
from app.groups.models import Group


class Entity(models.Model):
    # Stores the parent Id number of an entity, can have no pid making it the top most entity on a chart
    pid = models.CharField(
        max_length=50,
        blank=True
    )

    name = models.CharField(
        max_length=150
    )

    # Legal Forms will need to be a dropdown, will be used later to auto generate tax consequences
    # Each entity can only have ONE legal form
    legal_form = models.CharField(
        max_length=50
    )

    # Each entity can only have ONE location ( possibly two, if we differentiate between legal residence and country of tax residence )
    # Alain wants to leave this at one location at this time
    location = models.CharField(
        max_length=50
    )

    # Needs to store decimal tax rates ( i.e. 0.1259 = 12.59% )
    tax_rate = models.DecimalField(
        max_digits=5,
        decimal_places=4,
        blank=True,
        null=True
    )

    # Stores if a Entity is currently part of a Group, inactive entities have been deleted, liquidated, or are part of an uncompleted project
    active = models.BooleanField(
        default=True
    )

    created = models.DateTimeField(
        auto_now_add=True
    )

    updated = models.DateTimeField(
        auto_now=True
    )

    group = models.ForeignKey(
        to=Group,
        on_delete=models.CASCADE,
        related_name='entities',
        null=True,
        blank=True
    )

    def __str__(self):
        return f'Entity #{self.pk} - Name: {self.name} for Group: {self.group.name}'
