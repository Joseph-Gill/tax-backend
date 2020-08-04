from django.dispatch import receiver
from django_extensions.db.models import TimeStampedModel
from django.conf import settings
from django.db import models
import random

from app.registration.signals import post_user_social_registration


def code_generator(length=5):
    numbers = '0123456789'
    return ''.join(random.choice(numbers) for _ in range(length))


class RegistrationProfile(TimeStampedModel):
    user = models.OneToOneField(
        verbose_name='user',
        on_delete=models.CASCADE,
        related_name='registration_profile',
        to=settings.AUTH_USER_MODEL
    )
    code = models.CharField(
        verbose_name='code',
        help_text='random code used for registration and for password reset',
        max_length=15,
        default=code_generator
    )
    code_type = models.CharField(
        verbose_name='code type',
        max_length=2,
        choices=(
            ('RV', 'Registration Validation'),
            ('PR', 'Password Reset')
        )
    )
    code_used = models.BooleanField(
        verbose_name='code used',
        default=False
    )

    def __str__(self):
        return f'{self.user.email}, {self.code}'


# Users registered through social auth need a registration profile in case they want to login with the standard credentials => they need to be able to set / reset a password
@receiver(post_user_social_registration)
def create_registration_profile(sender, user, **kwargs):
    RegistrationProfile(user=user, code_type='RV', code_used=True).save()
