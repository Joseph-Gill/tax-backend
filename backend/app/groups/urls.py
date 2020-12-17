from django.urls import path
from app.groups.views import ListAllOrCreateGroup, RetrieveUpdateDestroySpecificGroup, ListAllUsersGroups, AddUserInSpecificGroup, DestroyUserFromNewUserList, RemoveUsersFromGroupAndProjects

urlpatterns = [
    path('', ListAllOrCreateGroup.as_view(), name='list-create-group'),
    path('me/', ListAllUsersGroups.as_view(), name='list-user-groups'),
    path('group/<int:group_id>/', RetrieveUpdateDestroySpecificGroup.as_view(), name='retrieve-update-destroy-group'),
    path('group/<int:group_id>/user/', AddUserInSpecificGroup.as_view(), name='add-remove-user-group'),
    path('group/<int:group_id>/newuser/', DestroyUserFromNewUserList.as_view(), name='destroy-new-user-in-group-list'),
    path('group/<int:group_id>/removeusers/', RemoveUsersFromGroupAndProjects.as_view(), name='destroy-users-from-group-and-projects')
]