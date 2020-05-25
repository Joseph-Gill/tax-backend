# Generated by Django 3.0.2 on 2020-03-17 16:09

from django.db import migrations, models
import django_extensions.db.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.CharField(max_length=1000, verbose_name='comment')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='created time')),
            ],
            options={
                'ordering': ['-created'],
            },
        ),
        migrations.CreateModel(
            name='Friend',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('status', models.CharField(choices=[('P', 'Pending'), ('A', 'Accepted'), ('R', 'Rejected')], default='P', max_length=1, verbose_name='status')),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(verbose_name='content')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='created')),
            ],
        ),
        migrations.CreateModel(
            name='SocialProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('avatar', models.ImageField(blank=True, upload_to='')),
                ('location', models.CharField(blank=True, max_length=200, verbose_name='user location')),
                ('about_me', models.CharField(blank=True, max_length=1000, verbose_name='user description')),
                ('job', models.CharField(blank=True, max_length=200, verbose_name='job title')),
                ('followees', models.ManyToManyField(blank=True, related_name='followers', to='social.SocialProfile', verbose_name='followees')),
                ('liked_posts', models.ManyToManyField(blank=True, related_name='liked_by', to='social.Post', verbose_name='liked posts')),
            ],
            options={
                'ordering': ('-modified', '-created'),
                'get_latest_by': 'modified',
                'abstract': False,
            },
        ),
    ]
