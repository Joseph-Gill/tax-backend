from django.contrib import admin

from app.notifications.models import NotificationProfile, NotificationTypes

admin.site.register(NotificationProfile)
admin.site.register(NotificationTypes)
