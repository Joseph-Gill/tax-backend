# Generated by Django 3.0.2 on 2021-05-05 14:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('entities', '0001_initial'),
        ('entityHistories', '0002_entityhistory_creator'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='entityhistory',
            name='affected_entities',
        ),
        migrations.AddField(
            model_name='entityhistory',
            name='affected_entities',
            field=models.ManyToManyField(blank=True, related_name='affected_histories', to='entities.Entity'),
        ),
    ]
