from django.conf import settings
from django.db import models
from django.dispatch import receiver
from django.template import Template, Context
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
        to='notifications.NotificationType',
        related_name='subscribed_user_notification_profiles',
        blank=True
    )

    def __str__(self):
        return self.user.email


class NotificationType(models.Model):
    key = models.CharField(
        verbose_name='notification key',
        max_length=200
    )
    subject = models.CharField(
        verbose_name='subject',
        max_length=200
    )
    title = models.CharField(
        verbose_name='title',
        max_length=200
    )
    description = models.TextField(
        verbose_name='description'
    )
    template = models.TextField(
        verbose_name='template extension',
        default="{% extends 'mail_base.html' %} \n {% block extension %} \n {% endblock %}"
    )

    def __str__(self):
        return self.key


@receiver(notify_users)
def send_notifications(sender, notification_key, **kwargs):
    try:
        notification_type = NotificationType.objects.get(key=notification_key)
        for user_notification_profile in notification_type.subscribed_user_notification_profiles.all():
            request = kwargs.pop('request', None)
            context = {
                'title': notification_type.title,
                'description': notification_type.description,
                **kwargs
            }
            c = Context(context)
            c.request = request
            t = Template(notification_type.template)

            body = t.render(c)

            Email(
                to=user_notification_profile.user.email,
                subject=notification_type.subject,
                content=notification_type.description,
                compiled_template=body
            ).save()
    except NotificationType.DoesNotExist:
        pass


@receiver(post_user_registration_validation)
def create_social_profile(sender, user, **kwargs):
    if user.is_superuser or user.is_staff:
        NotificationProfile(user=user).save()
