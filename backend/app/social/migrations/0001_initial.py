# Generated by Django 2.2.2 on 2019-11-05 09:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_extensions.db.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(verbose_name='content')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='created')),
                ('shared', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='sharing_posts', to='social.Post', verbose_name='shared post')),
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
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='social_profile', to=settings.AUTH_USER_MODEL, verbose_name='user')),
            ],
            options={
                'ordering': ('-modified', '-created'),
                'get_latest_by': 'modified',
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='post',
            name='social_profile',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='posts', to='social.SocialProfile', verbose_name='social user profile'),
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.CharField(max_length=1000, verbose_name='comment')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='created time')),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='social.Post', verbose_name='post')),
                ('social_profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='social.SocialProfile', verbose_name='user')),
            ],
            options={
                'ordering': ['-created'],
            },
        ),
    ]
