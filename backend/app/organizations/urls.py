from django.urls import path

from app.organizations.views import ListAllOrCreateOrganization, RetrieveUpdateDestroySpecificOrganization

urlpatterns = [
    path('', ListAllOrCreateOrganization.as_view(), name='list-create-organization'),
    path('org/<int:org_id>', RetrieveUpdateDestroySpecificOrganization.as_view(), name='retrieve-update-destroy-organization')
]