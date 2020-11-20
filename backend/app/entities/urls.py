from django.urls import path

from app.entities.views import ListAllOrCreateEntity, RetrieveUpdateDestroySpecificEntity

urlpatterns = [
    path('', ListAllOrCreateEntity.as_view(), name='list-create-entity'),
    path('entity/<int:entity_id>/', RetrieveUpdateDestroySpecificEntity.as_view(), name='retrieve-update-destroy-entity')
]