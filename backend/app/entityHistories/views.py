from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework import status
from app.charts.models import Chart
from app.entities.models import Entity
from app.entityHistories.models import EntityHistory
from app.entityHistories.serializers import EntityHistorySerializer
from app.userProfiles.models import UserProfile
import json


class CreateEntityHistoryForChart(CreateAPIView):
    """
    Create a new Entity History for a specified Entity and specified Chart
    """
    queryset = Chart.objects.all()
    lookup_url_kwarg = 'chart_id'
    serializer_class = EntityHistorySerializer

    def create(self, request, *args, **kwargs):
        users_profile = UserProfile.objects.get(user=self.request.user)
        target_chart = self.get_object()
        target_entity = Entity.objects.get(id=kwargs['entity_id'])
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        # Creates the history for the entity that was the source of the action
        new_entity_history = EntityHistory(
            action=serializer.validated_data.get('action'),
            entity=target_entity,
            chart=target_chart,
            creator=users_profile
        )
        new_entity_history.save()
        # Provides a list of entities that were affected by this action
        list_of_affected_entities = json.loads(self.request.data['affected'])
        for entity in list_of_affected_entities:
            # Gets the entity that was affected by this action
            target_affected_entity = Entity.objects.get(id=entity)
            # Stores the second half of the action for affected entities i.e. add_entity_CHILD, distribution_PARTICIPANT, etc...
            keyword = request.data['affected_keyword']
            affected_entity_history = EntityHistory(
                action=f'{new_entity_history.action}_{keyword}',
                entity=target_affected_entity,
                chart=target_chart,
                creator=users_profile
            )
            affected_entity_history.save()
            new_entity_history.affected_entities.add(target_affected_entity)
        return_data = self.get_serializer(new_entity_history)
        return Response(return_data.data, status=status.HTTP_201_CREATED)
