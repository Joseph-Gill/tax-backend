from django.contrib import admin

from app.tasks.models import Task

admin.site.register(Task)
