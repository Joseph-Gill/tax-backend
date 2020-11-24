from django.urls import path

from app.organizations.views import ListAllOrCreateOrganizationForGroup, RetrieveUpdateDestroySpecificOrganization

urlpatterns = [
    path('<int:group_id>/', ListAllOrCreateOrganizationForGroup.as_view(), name='list-create-organization'),
    path('org/<int:org_id>/', RetrieveUpdateDestroySpecificOrganization.as_view(), name='retrieve-update-destroy-organization')
]