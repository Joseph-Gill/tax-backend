from django.template import Context, Template

from app.celery import app
from app.emails.models import Email, EmailType
from django.conf import settings


@app.task
def send_registration_email_task(logo_url, to, email_type_key, **kwargs):
    email_type = EmailType.objects.get(key=email_type_key)
    context = {
        'title': email_type.title,
        'logo_url': logo_url,
        **kwargs
    }
    c = Context(context)
    t = Template(f'{settings.DEFAULT_EXTENSION_TEMPLATE_START}{email_type.template}{settings.DEFAULT_EXTENSION_TEMPLATE_END}')

    body = t.render(c)

    email = Email(
        to=to,
        subject=email_type.subject,
        compiled_template=body
    )
    email.save()
    email.send()
