# Generated by Django 3.0.2 on 2021-05-13 15:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('entityHistories', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entityhistory',
            name='creating_action',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='affected_entities', to='entityHistories.EntityHistory'),
        ),
    ]
