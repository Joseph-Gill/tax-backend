from django.template import Context, Template
from django.apps import apps
from app.celery import app
from app.emails.models import Email

DEFAULT_EXTENSION_TEMPLATE_START = "{% extends 'mail_base.html' %} \n {% block extension %} \n "
DEFAULT_EXTENSION_TEMPLATE_END = "\n {% endblock %}"


@app.task
def send_notification_task(notification_key, **kwargs):
    try:
        NotificationType = apps.get_model('notifications', 'NotificationType')  # need to import model like this or get circular import
        notification_type = NotificationType.objects.get(key=notification_key)
        for user_notification_profile in notification_type.subscribed_user_notification_profiles.all():
            context = {
                'title': notification_type.title,
                'description': notification_type.description,
                **kwargs
            }
            c = Context(context)
            t = Template(f'{DEFAULT_EXTENSION_TEMPLATE_START}{notification_type.template}{DEFAULT_EXTENSION_TEMPLATE_END}')

            body = t.render(c)

            Email(
                to=user_notification_profile.user.email,
                subject=notification_type.subject,
                content=notification_type.description,
                compiled_template=body
            ).save()
    except NotificationType.DoesNotExist:
        pass


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
