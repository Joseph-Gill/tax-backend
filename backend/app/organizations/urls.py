from django.urls import path

from app.organizations.views import ListAllOrCreateOrganizationForGroup, RetrieveUpdateDestroySpecificOrganization, RetrieveOrganizationForSpecificUserGroup

urlpatterns = [
    path('<int:group_id>/', ListAllOrCreateOrganizationForGroup.as_view(), name='list-create-organization'),
    path('org/<int:org_id>/', RetrieveUpdateDestroySpecificOrganization.as_view(), name='retrieve-update-destroy-organization'),
    path('group/<int:group_id>/user/<int:user_id>/', RetrieveOrganizationForSpecificUserGroup.as_view(), name='retrieve-org-specific-user-group')
]
