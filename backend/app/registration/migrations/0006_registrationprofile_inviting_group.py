# Generated by Django 3.0.2 on 2021-05-05 11:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('groups', '0001_initial'),
        ('registration', '0005_auto_20201118_1547'),
    ]

    operations = [
        migrations.AddField(
            model_name='registrationprofile',
            name='inviting_group',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='invited_new_users', to='groups.Group'),
        ),
    ]
