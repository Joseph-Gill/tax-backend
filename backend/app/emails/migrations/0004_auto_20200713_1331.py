# Generated by Django 3.0.2 on 2020-07-13 11:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('emails', '0003_auto_20200525_1733'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='email',
            options={'get_latest_by': 'modified'},
        ),
    ]