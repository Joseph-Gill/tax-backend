from django.urls import path

from app.steps.views import ListAllOrCreateStepForSpecificProject, RetrieveUpdateDestroySpecificStep, RetrieveProjectStepsStatusNumbers, RetrieveProjectFirstUncompletedStep, UpdateStepSetStepAsCompleted

urlpatterns = [
    path('project/<int:project_id>/', ListAllOrCreateStepForSpecificProject.as_view(), name='list-create-step'),
    path('step/<int:step_id>/', RetrieveUpdateDestroySpecificStep.as_view(), name='retrieve-update-destroy-step'),
    path('project/<int:project_id>/statusnumbers/', RetrieveProjectStepsStatusNumbers.as_view(), name='retrieve-project-steps-status-numbers'),
    path('project/<int:project_id>/firstuncompleted/', RetrieveProjectFirstUncompletedStep.as_view(), name='retrieve-project-first-uncompleted-step'),
    path('step/<int:step_id>/completed/', UpdateStepSetStepAsCompleted.as_view(), name='updated-set-step-completed')
]
