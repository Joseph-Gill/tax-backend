from django.urls import path

from app.projects.views import ListAllOrCreateProjectForSpecificGroup, RetrieveUpdateDestroySpecificProject

urlpatterns = [
    path('<int:group_id>/', ListAllOrCreateProjectForSpecificGroup.as_view(), name='list-create-project'),
    path('/project/<int:project_id>/', RetrieveUpdateDestroySpecificProject.as_view(), name='retrieve-update-destroy-project')
]
