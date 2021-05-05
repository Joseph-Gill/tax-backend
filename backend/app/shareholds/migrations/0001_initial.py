# Generated by Django 3.0.2 on 2021-05-05 11:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('entities', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Sharehold',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('percent_ownership', models.DecimalField(blank=True, decimal_places=4, max_digits=5, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('child', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shareholds_child', to='entities.Entity')),
                ('parent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shareholds_parent', to='entities.Entity')),
            ],
        ),
    ]
