# Generated by Django 3.0.2 on 2021-05-05 11:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('groups', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Entity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pid', models.CharField(blank=True, max_length=50)),
                ('name', models.CharField(max_length=150)),
                ('legal_form', models.CharField(max_length=50)),
                ('location', models.CharField(max_length=50)),
                ('tax_rate', models.DecimalField(blank=True, decimal_places=4, max_digits=5, null=True)),
                ('active', models.BooleanField(default=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('group', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='entities', to='groups.Group')),
            ],
        ),
    ]
