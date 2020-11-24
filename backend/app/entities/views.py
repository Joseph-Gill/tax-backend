from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView

from app.entities.models import Entity
from app.entities.serializers import EntitySerializer


class ListAllOrCreateEntityForGroup(ListCreateAPIView):
    """
    get:
    List all Entities

    post:
    Create a new Entity
    """
    pass


class RetrieveUpdateDestroySpecificEntity(RetrieveUpdateDestroyAPIView):
    """
    get:
    List a specified Entity

    update:
    Update a specified Entity

    delete:
    Delete a specified Entity
    """
    http_method_names = ['get', 'patch', 'delete']
    serializer_class = EntitySerializer
    queryset = Entity.objects.all()
    lookup_url_kwarg = 'entity_id'
