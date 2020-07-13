from django.dispatch import receiver
from django_extensions.db.models import TimeStampedModel
from django.conf import settings
from django.db import models

from app.registration.signals import post_user_registration_validation
from app.social.models import Friend, Post


class SocialProfile(TimeStampedModel):
    user = models.OneToOneField(
        verbose_name='user',
        on_delete=models.CASCADE,
        related_name='social_profile',
        to=settings.AUTH_USER_MODEL
    )
    upload_avatar = models.ImageField(
        upload_to='',
        blank=True,
    )
    social_avatar = models.URLField(
        max_length=2000,
        blank=True
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

    # @property
    # def avatar(self):
    #     if hasattr(self.upload_avatar, 'url'):
    #         return self.upload_avatar.url
    #     elif self.social_avatar:
    #         return self.social_avatar
    #     else:
    #         return None

    @property
    def friends(self):
        friends_profiles = []

        received_requests = Friend.objects.filter(
            receiver=self,
            status='A'
        )
        for friend in received_requests:
            friends_profiles.append(friend.requester)
        requested_requests = Friend.objects.filter(
            requester=self,
            status='A'
        )
        for friend in requested_requests:
            friends_profiles.append(friend.receiver)
        return friends_profiles

    def __str__(self):
        return f'{self.user.email}'


@receiver(post_user_registration_validation)
def create_social_profile(sender, user, **kwargs):
    SocialProfile(user=user).save()
