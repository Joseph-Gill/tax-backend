from django.urls import path
from app.projectRoles.views import ListRolesForSpecifiedUserProfileGroup, ListAllUsersWithRoleForSpecifiedProject, ToggleUserFavoriteProjectStatus

urlpatterns = [
    path('userprofile/<int:userprofile_id>/group/<int:group_id>/', ListRolesForSpecifiedUserProfileGroup.as_view(), name='retrieve-roles-user-group'),
    path('group/<int:group_id>/project/<int:project_id>/', ListAllUsersWithRoleForSpecifiedProject.as_view(), name='retrieve-roles-group-project'),
    path('userprofile/<int:userprofile_id>/project/<int:project_id>/', ToggleUserFavoriteProjectStatus.as_view(), name='toggle-favorite-project')
]
