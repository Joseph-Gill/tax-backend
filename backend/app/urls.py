from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from rest_framework.documentation import include_docs_urls

api_patterns = [
    path('users/', include('app.users.urls')),
    path('social/', include('app.social.urls')),
    path('auth/', include('app.registration.urls')),
    path('notifications/', include('app.notifications.urls')),
    path('feedback/', include('app.feedback.urls')),
    path('contact/', include('app.contact.urls')),

    path('docs/', include_docs_urls(title='Django Template', permission_classes=[])),

]

urlpatterns = [
    path('backend/true-admin/', admin.site.urls),  # please change this url for security
    path('backend/admin/', include('admin_honeypot.urls', namespace='admin_honeypot')),
    path('backend/api/', include(api_patterns)),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
