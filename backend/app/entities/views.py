from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from app.entities.models import Entity
from app.entities.serializers import EntitySerializer
from app.groups.models import Group


class ListAllOrCreateEntityForGroup(ListCreateAPIView):
    """
    get:
    List all Entities

    post:
    Create a new Entity
    """
    queryset = Group
    serializer_class = EntitySerializer
    lookup_url_kwarg = 'group_id'
    permission_classes = []

    def list(self, request, *args, **kwargs):
        target_group = self.get_object()
        entities = target_group.entities.all().order_by('pid')
        serializer = self.get_serializer(entities, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        target_group = self.get_object()
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        new_entity = Entity(
            **serializer.validated_data,
            active=False
        )
        new_entity.save()
        target_group.entities.add(new_entity)
        return_data = self.get_serializer(new_entity)
        return Response(return_data.data, status=status.HTTP_201_CREATED)


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
