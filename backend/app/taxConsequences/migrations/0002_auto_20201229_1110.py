# Generated by Django 3.0.2 on 2020-12-29 10:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('userProfiles', '0002_userprofile_country'),
        ('taxConsequences', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='taxconsequence',
            name='creating_user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_tax_consequences', to='userProfiles.UserProfile'),
        ),
        migrations.AddField(
            model_name='taxconsequence',
            name='reviewed',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='taxconsequence',
            name='reviewing_user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='reviewed_tax_consequences', to='userProfiles.UserProfile'),
        ),
    ]