from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework import status
from app.charts.models import Chart
from app.entities.models import Entity
from app.entityHistories.models import EntityHistory
from app.entityHistories.serializers import EntityHistorySerializer


class CreateEntityHistoryForChart(CreateAPIView):
    """
    Create a new Entity History for a specified Entity and specified Chart
    """
    queryset = Chart.objects.all()
    lookup_url_kwarg = 'chart_id'
    serializer_class = EntityHistorySerializer

    def create(self, request, *args, **kwargs):
        target_chart = self.get_object()
        target_entity = Entity.objects.get(id=kwargs['entity_id'])
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        new_entity_history = EntityHistory(
            **serializer.validated_data,
            entity=target_entity,
            chart=target_chart
        )
        new_entity_history.save()
        return_data = self.get_serializer(new_entity_history)
        return Response(return_data.data, status=status.HTTP_201_CREATED)
