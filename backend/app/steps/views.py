from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, RetrieveAPIView
from rest_framework.response import Response
from app.projects.models import Project
from app.steps.models import Step
from app.steps.serializers import StepSerializer


class ListAllOrCreateStepForSpecificProject(ListCreateAPIView):
    """
    get:
    List all Steps for a specified Project

    post:
    Create a new Step for a specified Project
    """
    queryset = Project
    serializer_class = StepSerializer
    lookup_url_kwarg = 'project_id'
    permission_classes = []

    def list(self, request, *args, **kwargs):
        target_project = self.get_object()
        steps = target_project.steps.all().order_by('number')
        serializer = self.get_serializer(steps, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        target_project = self.get_object()
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        new_step = Step(
            **serializer.validated_data
        )
        new_step.save()
        target_project.steps.add(new_step)
        return Response(status=status.HTTP_201_CREATED)


class RetrieveUpdateDestroySpecificStep(RetrieveUpdateDestroyAPIView):
    """
    get:
    List a specified Step

    update:
    Update a specified Step

    delete:
    Delete a specified Step
    """
    http_method_names = ['get', 'patch', 'delete']
    serializer_class = StepSerializer
    queryset = Step.objects.all()
    lookup_url_kwarg = 'step_id'


class RetrieveProjectStepsStatusNumbers(RetrieveAPIView):
    queryset = Project.objects.all()
    lookup_url_kwarg = 'project_id'

    def retrieve(self, request, *args, **kwargs):
        target_project = self.get_object()
        step_status_results = {
            "Ongoing": 0,
            "Planned": 0,
            "Completed": 0,
            "Not Started": 0
        }
        for step in target_project.steps.all():
            step_status_results[step.status] = step_status_results[step.status] + 1
        return Response(step_status_results, status=status.HTTP_200_OK)
