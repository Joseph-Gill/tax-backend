from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
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
