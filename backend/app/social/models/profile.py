from django_extensions.db.models import TimeStampedModel
from django.conf import settings
from django.db import models


class SocialProfile(TimeStampedModel):
    user = models.OneToOneField(
        verbose_name='user',
        on_delete=models.CASCADE,
        related_name='social_profile',
        to=settings.AUTH_USER_MODEL
    )

    def __str__(self):
        return f'{self.user.email}, {self.code}'
