from django.urls import path

from app.entities.views import ListAllOrCreateEntityForGroup, RetrieveUpdateDestroySpecificEntity

urlpatterns = [
    path('<int:group_id>/', ListAllOrCreateEntityForGroup.as_view(), name='list-create-entity'),
    path('entity/<int:entity_id>/', RetrieveUpdateDestroySpecificEntity.as_view(), name='retrieve-update-destroy-entity')
]