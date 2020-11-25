from rest_framework import status
from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListAPIView, CreateAPIView
from rest_framework.response import Response

from app.charts.models import Chart
from app.charts.serializers import ChartSerializer
from app.steps.models import Step


class CreateChartForSpecificProjectStep(CreateAPIView):
    """
    Create a Chart for a specified Project Step
    """
    queryset = Step
    serializer_class = ChartSerializer
    lookup_url_kwarg = 'step_id'
    permission_classes = []

    def create(self, request, *args, **kwargs):
        target_step = self.get_object()
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        new_chart = Chart(
            **serializer.validated_data,
            step=target_step
        )
        new_chart.save()
        return Response(status=status.HTTP_201_CREATED)


class RetrieveUpdateDestroySpecificChart(RetrieveUpdateDestroyAPIView):
    """
    get:
    List a specified Chart

    update:
    Update a specified Chart

    delete:
    Delete a specified Chart
    """
    http_method_names = ['get', 'patch', 'delete']
    serializer_class = ChartSerializer
    queryset = Chart.objects.all()
    lookup_url_kwarg = 'chart_id'
