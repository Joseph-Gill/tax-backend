from django_extensions.db.models import TimeStampedModel
from django.conf import settings
from django.db import models
from app.social.models.posts import Post


class SocialProfile(TimeStampedModel):
    user = models.OneToOneField(
        verbose_name='user',
        on_delete=models.CASCADE,
        related_name='social_profile',
        to=settings.AUTH_USER_MODEL
    )
    avatar = models.ImageField(
        upload_to='',
        blank=True,
    )

    location = models.CharField(
        verbose_name='user location',
        max_length=200,
        blank=True
    )

    about_me = models.CharField(
        verbose_name='user description',
        max_length=1000,
        blank=True
    )

    job = models.CharField(
        verbose_name='job title',
        max_length=200,
        blank=True
    )

    followees = models.ManyToManyField(
        verbose_name='followees',
        to='SocialProfile',
        related_name='followers',
        blank=True,
    )

    liked_posts = models.ManyToManyField(
        verbose_name='liked posts',
        to=Post,
        related_name='liked_by',
        blank=True,

    )

    def __str__(self):
        return f'{self.user.email}'