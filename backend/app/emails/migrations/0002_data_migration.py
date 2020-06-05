# Generated by Django 3.0.2 on 2020-01-23 14:16

from django.db import migrations


def populate_db(apps, schema_editor):
    # Dev Emails
    dev_emails = ['SignalFlux@outlook.com', 'danieler@propulsionacademy.com', 'rubenv@propulsionacademy.com', 'cedricd@propulsionacademy.com', 'sebastianm@propulsionacademy.com']
    DevEmail = apps.get_model('emails', 'DevEmails')
    for email in dev_emails:
        DevEmail(email=email).save()

    # Email Types
    email_types = [
        {
            "key": "registration_email",
            "subject": "Subject: Thank you for registering!",
            "title": "Title: Thank you for registering!",
            "template": "Click <a href='{{ pure_url }}registration-validation?code={{code}}'> here</a> to finalize registration."
        },
        {
            "key": "password_reset_email",
            "subject": "Subject: Password reset",
            "title": "Title: Password reset",
            "template": "Click <a href='{{ pure_url }}password-reset-validation?code={{code}}'>  here</a> to reset your password:"
        },
    ]
    EmailType = apps.get_model('emails', 'EmailType')
    for email_type in email_types:
        EmailType(**email_type).save()




class Migration(migrations.Migration):
    dependencies = [
        ('emails', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(populate_db),
    ]
