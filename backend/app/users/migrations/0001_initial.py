# Generated by Django 2.2.2 on 2019-10-11 12:06

import app.users.models
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
        ('post', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('username', models.CharField(max_length=200, unique=True, verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=200, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=200, verbose_name='first name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('timestamp', models.DateTimeField(auto_now_add=True, verbose_name='date joined')),
                ('avatar', models.ImageField(blank=True, default='media-files/avatar.jpg', upload_to='media-files/')),
                ('location', models.CharField(blank=True, max_length=200, verbose_name='user location')),
                ('about_me', models.CharField(blank=True, max_length=1000, verbose_name='user description')),
                ('job', models.CharField(blank=True, max_length=200, verbose_name='job title')),
                ('code', models.CharField(default=app.users.models.code_generator, help_text='random code used for registration and for password reset', max_length=15, verbose_name='code')),
                ('bookmarked_posts', models.ManyToManyField(blank=True, related_name='bookmarked_by', to='post.Post', verbose_name='bookmarked posts')),
                ('followees', models.ManyToManyField(blank=True, related_name='followers', to=settings.AUTH_USER_MODEL, verbose_name='following')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
