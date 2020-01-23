# Generated by Django 3.0.2 on 2020-01-23 14:16

from django.db import migrations


def populate_db(apps, schema_editor):
    # Dev Emails
    dev_emails = ['SignalFlux@outlook.com', 'danieler@propulsionacademy.com', 'rubenv@propulsionacademy.com', 'cedricd@propulsionacademy.com']
    DevEmail = apps.get_model('emails', 'DevEmails')
    for email in dev_emails:
        DevEmail(email=email).save()

    # Email Types
    email_types = [
        {
            "key": "registration_email",
            "subject": "Subject: Thank you for registering!",
            "title": "Title: Thank you for registering!",
            "template": "Here is your validation code: {{code}}"
        },
        {
            "key": "password_reset_email",
            "subject": "Subject: Password reset",
            "title": "Title: Password reset",
            "template": "Here is your password reset code: {{code}}"
        },
    ]
    EmailType = apps.get_model('emails', 'EmailType')
    for email_type in email_types:
        EmailType(**email_type).save()




class Migration(migrations.Migration):
    dependencies = [
        ('emails', '0002_auto_20200120_1800'),
    ]

    operations = [
        migrations.RunPython(populate_db),
    ]
