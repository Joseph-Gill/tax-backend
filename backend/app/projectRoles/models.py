from django.db import models


class ProjectRole(models.Model):
    # Role choices are Core, Legal, Tax, Other
    role = models.CharField(
        max_length=10
    )

    created = models.DateTimeField(
        auto_now_add=True
    )

    updated = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return f'Project Role #{self.pk} for User - {self.registration_profile.user.email}'
