# Generated by Django 3.0.2 on 2020-12-21 16:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userProfiles', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='country',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
