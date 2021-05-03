# Generated by Django 3.0.2 on 2021-05-03 13:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('charts', '0001_initial'),
        ('entities', '0004_auto_20210503_1543'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entity',
            name='charts',
            field=models.ManyToManyField(blank=True, related_name='entities', to='charts.Chart'),
        ),
    ]