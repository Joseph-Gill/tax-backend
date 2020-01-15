from django.template import Context, Template
from django.apps import apps
from app.celery import app
from app.emails.models import Email


@app.task(typing=False)
def send_notification_task(notification_key, **kwargs):
    print('lalallalallalallallalalalalallalallalallallalallala', notification_key)
    # try:
    #     NotificationType = apps.get_model('notifications', 'NotificationType')
    #     notification_type = NotificationType.objects.get(key=notification_key)
    #     for user_notification_profile in notification_type.subscribed_user_notification_profiles.all():
    #         request = kwargs.pop('request', None)
    #         context = {
    #             'title': notification_type.title,
    #             'description': notification_type.description,
    #             **kwargs
    #         }
    #         c = Context(context)
    #         c.request = request
    #         t = Template(notification_type.template)
    #
    #         body = t.render(c)
    #
    #         Email(
    #             to=user_notification_profile.user.email,
    #             subject=notification_type.subject,
    #             content=notification_type.description,
    #             compiled_template=body
    #         ).save()
    # except NotificationType.DoesNotExist:
    #     pass
