# Generated by Django 3.0.2 on 2020-11-18 14:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0004_auto_20200717_0946'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='registrationprofile',
            options={'get_latest_by': 'modified'},
        ),
    ]
