from django.conf import settings
from django.db import models
from django.dispatch import receiver
from django.template.loader import render_to_string

from app.emails.models import Email
from app.notifications.signals import notify_users
from app.registration.signals import post_user_registration_validation


class NotificationProfile(models.Model):
    user = models.OneToOneField(
        verbose_name='user',
        on_delete=models.CASCADE,
        related_name='notification_profile',
        to=settings.AUTH_USER_MODEL
    )
    subscribed_notification_types = models.ManyToManyField(
        verbose_name='subscribed notification types',
        to='notifications.NotificationTypes',
        related_name='subscribed_user_notification_profiles',
        blank=True
    )

    def __str__(self):
        return self.user.email


class NotificationTypes(models.Model):
    key = models.CharField(
        verbose_name='notification key',
        max_length=200
    )
    subject = models.CharField(
        verbose_name='subject',
        max_length=200
    )
    description = models.TextField(
        verbose_name='description'
    )

    def __str__(self):
        return self.key


@receiver(notify_users)
def send_notifications(sender, notification_key, **kwargs):
    try:
        notification_type = NotificationTypes.objects.get(key=notification_key)
        for user_notification_profile in notification_type.subscribed_user_notification_profiles.all():
            context = {
                'title': notification_type.subject,
                'description': notification_type.description,
            }
            body = render_to_string(
                template_name=f'mail_base.html',
                context=context,
                request=kwargs['request']
            )
            Email(
                to=user_notification_profile.user.email,
                subject=notification_type.subject,
                content=notification_type.description,
                compiled_template=body
            ).save()
    except NotificationTypes.DoesNotExist:
        pass


@receiver(post_user_registration_validation)
def create_social_profile(sender, user, **kwargs):
    NotificationProfile(user=user).save()
