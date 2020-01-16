from django.conf import settings
from django.core.mail import EmailMessage
from django.db import models
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
from django_extensions.db.models import TimeStampedModel


class DevEmails(models.Model):
    email = models.EmailField(
        verbose_name='dev email'
    )

    def __str__(self):
        return self.email


class Email(TimeStampedModel):
    template_name = 'mail_base.html'

    to = models.EmailField(
        verbose_name='To',
    )
    subject = models.CharField(
        verbose_name='Subject',
        max_length=200,
    )
    content = models.TextField(
        verbose_name='Content',
    )
    compiled_template = models.TextField(
        verbose_name='compiled_template',
        blank=True,
    )
    bcc = models.TextField(
        verbose_name='bcc',
        blank=True,
    )
    is_sent = models.BooleanField(
        verbose_name='is_sent',
        default=False,
    )

    def save(self, **kwargs):
        if not self.compiled_template:
            request = kwargs.pop('request')
            context = {
                'title': self.subject,
                'description': self.content,
                'logo_url': request.build_absolute_uri(settings.STATIC_URL)
            }
            body = render_to_string(
                template_name=self.template_name,
                context=context
            )
            self.compiled_template = body
        super().save(**kwargs)

    def send(self):
        if not settings.DEBUG or len(DevEmails.objects.filter(email=self.to)) > 0:
            message = EmailMessage(
                subject=self.subject,
                body=mark_safe(self.compiled_template),
                to=self.to.split(','),
                bcc=self.bcc.split(',')
            )
            message.content_subtype = "html"
            message.send()
            self.is_sent = True
            self.save()

    def __str__(self):
        return f'{self.to} - {self.subject}'
