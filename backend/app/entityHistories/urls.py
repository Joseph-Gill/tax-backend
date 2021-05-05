from django.urls import path
from app.entityHistories.views import CreateEntityHistoryForChart

urlpatterns = [
    path('entity/<int:entity_id>/chart/<int:chart_id>/', CreateEntityHistoryForChart.as_view(), name='create-entity-history'),
]