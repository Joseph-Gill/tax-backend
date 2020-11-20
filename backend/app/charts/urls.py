from django.urls import path

from app.charts.views import ListAllChartsForSpecificProject, CreateChartForSpecificProjectStep, RetrieveUpdateDestroySpecificChart

urlpatterns = [
    path('<int:project_id>/', ListAllChartsForSpecificProject.as_view(), name='list-charts'),
    path('step/<int:step_id>/', CreateChartForSpecificProjectStep.as_view(), name='create-chart'),
    path('chart/<int:chart_id>/', RetrieveUpdateDestroySpecificChart.as_view(), name='retrieve-update-destroy-chart')
]