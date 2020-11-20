from django.urls import path

from app.tasks.views import ListAllOrCreateTaskForSpecificStep, RetrieveUpdateDestroySpecificTask

urlpatterns = [
    path('<int:step_id>/', ListAllOrCreateTaskForSpecificStep.as_view(), name='list-create-task'),
    path('task/<int:task_id>/', RetrieveUpdateDestroySpecificTask.as_view(), name='retrieve-update-destroy-task')
]