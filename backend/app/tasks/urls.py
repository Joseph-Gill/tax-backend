from django.urls import path
from app.tasks.views import ListAllTasksForSpecificStep, RetrieveUpdateDestroySpecificTask, CreateTaskForSpecificStepForSpecificUser, UpdateUserForSpecificTask, ListAllTasksForSpecifiedProject

urlpatterns = [
    path('<int:step_id>/', ListAllTasksForSpecificStep.as_view(), name='list-task'),
    path('task/<int:task_id>/', RetrieveUpdateDestroySpecificTask.as_view(), name='retrieve-update-destroy-task'),
    path('step/<int:step_id>/userprofile/<int:userprofile_id>/', CreateTaskForSpecificStepForSpecificUser.as_view(), name='create-task-step-user'),
    path('task/<int:task_id>/user/<int:user_id>/', UpdateUserForSpecificTask.as_view(), name='update-user-assigned-task'),
    path('project/<int:project_id>', ListAllTasksForSpecifiedProject.as_view(), name='list-tasks-project')
]