from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Templates API",
        default_version='v1',
        description="Backend API Template for Propulsion Academy Projects",
        terms_of_service="",
        contact=openapi.Contact(email="learn@propulsion-home.ch"),
        license=openapi.License(name="BSD License"),
    ),
    public=False,  # Set to False to enable Django Login to access docs
    permission_classes=(permissions.AllowAny,
                        #  permissions.IsAuthenticated,  # Uncomment to enable Authenticated access only to docs
                        ),
)
