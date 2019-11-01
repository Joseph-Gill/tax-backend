from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from rest_framework.documentation import include_docs_urls

urlpatterns = [
    path('backend/admin/', admin.site.urls),

    path('backend/api/users/', include('app.users.urls')),
    path('backend/api/posts/', include('app.post.urls')),
    path('backend/api/auth/', include('app.registration.urls')),

    path('backend/api/docs/', include_docs_urls(title='Kenntnis API', permission_classes=[])),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

