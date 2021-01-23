from django.urls import path

from app.charts.views import CreateChartForSpecificProjectStep, RetrieveUpdateDestroyChartForSpecificProjectStep

urlpatterns = [
    path('project/<int:project_id>/stepnumber/<int:step_number>/createchart/', CreateChartForSpecificProjectStep.as_view(), name='create-chart'),
    path('project/<int:project_id>/stepnumber/<int:step_number>/', RetrieveUpdateDestroyChartForSpecificProjectStep.as_view(), name='retrieve-update-destroy-chart')
]
