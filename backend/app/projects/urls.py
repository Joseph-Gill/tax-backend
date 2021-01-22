from django.urls import path

from app.projects.views import ListAllOrCreateProjectForSpecificGroup, RetrieveUpdateDestroySpecificProject, ListUsersWithAccessToProject

urlpatterns = [
    path('group/<int:group_id>/', ListAllOrCreateProjectForSpecificGroup.as_view(), name='list-create-project'),
    path('project/<int:project_id>/', RetrieveUpdateDestroySpecificProject.as_view(), name='retrieve-update-destroy-project'),
    path('project/<int:project_id>/accessusers/', ListUsersWithAccessToProject.as_view(), name='list-users-profiles-access-project')
]
