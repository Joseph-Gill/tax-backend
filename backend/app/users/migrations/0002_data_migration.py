# Generated by Django 3.0.2 on 2020-01-23 14:33

from django.db import migrations


def populate_db(apps, schema_editor):
    # Admin Users (password is adminadmin)
    users = [
        {
            "password": "pbkdf2_sha256$180000$vhb6N1Ec4Cx3$9ImBpPnZ2hc+nX9eJnvUndodMeu6Ictrv8CB7QYlAfI=",
            "last_login": "2020-01-17T10:43:57.385Z",
            "is_superuser": True,
            "email": "josephedwingill@gmail.com",
            "username": "josephg",
            "first_name": "Joseph",
            "last_name": "Gill",
            "is_staff": True,
            "is_active": True,
            "date_joined": "2020-01-08T16:24:25.428Z",
        }
    ]
    User = apps.get_model('users', 'User')
    for user in users:
        User(**user).save()


class Migration(migrations.Migration):
    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(populate_db),

    ]
