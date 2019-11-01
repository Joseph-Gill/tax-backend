# Generated by Django 2.2.2 on 2019-10-11 12:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ClapComment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='ClapPost',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='CodeSnippet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.TextField(blank=True, null=True, verbose_name='code snippet')),
                ('prog_language', models.CharField(blank=True, choices=[('JS', 'JAVASCRIPT'), ('PY', 'PYTHON'), ('HT', 'HTML'), ('CS', 'CSS')], default='JS', max_length=2, null=True)),
            ],
        ),
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
            name='Website',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.TextField(blank=True, null=True, verbose_name='link to share')),
                ('saved_website', models.TextField(blank=True, null=True)),
                ('title', models.TextField(blank=True, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('image_url', models.URLField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(verbose_name='content')),
                ('category', models.CharField(choices=[('FS', 'Full Stack'), ('FE', 'Frontend'), ('BE', 'Backend'), ('DS', 'Data Science')], default='FullStack', max_length=20, verbose_name='category')),
                ('check_to_save', models.BooleanField(default=False, verbose_name='Should the website be saved?')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='created')),
                ('code_snippet', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='post', to='post.CodeSnippet', verbose_name='code snippet')),
                ('shared', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='sharing_posts', to='post.Post', verbose_name='shared post')),
            ],
        ),
    ]
