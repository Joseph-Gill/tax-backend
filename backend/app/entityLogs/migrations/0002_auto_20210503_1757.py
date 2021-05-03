# Generated by Django 3.0.2 on 2021-05-03 15:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('entities', '0006_remove_entity_charts'),
        ('entityLogs', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='entitylog',
            name='temp_id',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='entitylog',
            name='entity',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='entity_logs', to='entities.Entity'),
        ),
    ]
