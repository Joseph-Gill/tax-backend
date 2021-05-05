from rest_framework import status
from rest_framework.generics import RetrieveUpdateDestroyAPIView, CreateAPIView
from rest_framework.response import Response
from app.charts.models import Chart
from app.charts.serializers import ChartSerializer
from app.projects.models import Project
from app.steps.models import Step


class CreateChartForSpecificProjectStep(CreateAPIView):
    """
    Create a Chart for a specified Project Step
    """
    queryset = Project.objects.all()
    lookup_url_kwarg = 'project_id'
    serializer_class = ChartSerializer

    def create(self, request, *args, **kwargs):
        target_project = self.get_object()
        target_step = Step.objects.get(project=target_project, number=kwargs['step_number'])
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        new_chart = Chart(
            **serializer.validated_data,
            step=target_step
        )
        new_chart.save()
        return_data = self.get_serializer(new_chart)
        return Response(return_data.data, status=status.HTTP_201_CREATED)


class RetrieveUpdateDestroyChartForSpecificProjectStep(RetrieveUpdateDestroyAPIView):
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
    queryset = Project.objects.all()
    lookup_url_kwarg = 'project_id'

    def retrieve(self, request, *args, **kwargs):
        target_project = self.get_object()
        try:
            target_chart = Chart.objects.get(step__number=kwargs['step_number'], step__project=target_project)
            serializer = self.get_serializer(target_chart)
            return Response(serializer.data)
        except Chart.DoesNotExist:
            return Response(status=status.HTTP_204_NO_CONTENT)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        target_project = self.get_object()
        target_chart = Chart.objects.get(step__number=kwargs['step_number'], step__project=target_project)
        serializer = self.get_serializer(target_chart, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)
