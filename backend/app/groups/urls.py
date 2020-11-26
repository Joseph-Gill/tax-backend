from django.urls import path

from app.groups.views import ListAllOrCreateGroup, RetrieveUpdateDestroySpecificGroup, ListAllUsersGroups, AddRemoveUserInSpecificGroup

urlpatterns = [
    path('', ListAllOrCreateGroup.as_view(), name='list-create-group'),
    path('me/', ListAllUsersGroups.as_view(), name='list-user-groups'),
    path('group/<int:group_id>/', RetrieveUpdateDestroySpecificGroup.as_view(), name='retrieve-update-destroy-group'),
    path('group/<int:group_id>/user/', AddRemoveUserInSpecificGroup.as_view(), name='add-remove-user-group')
]