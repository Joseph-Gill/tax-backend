from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, RetrieveAPIView, UpdateAPIView
from rest_framework.response import Response
from app.charts.models import Chart
from app.entities.models import Entity
from app.entityHistories.models import EntityHistory
from app.projects.models import Project
from app.steps.models import Step
from app.steps.serializers import StepSerializer
import json


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
    """
    Retrieve status numbers for all Steps of a specified Project
    """
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


class RetrieveProjectFirstUncompletedStep(RetrieveAPIView):
    """
    Retrieve the first step of a specified Project that is not "Completed" status
    """
    queryset = Project.objects.all()
    lookup_url_kwarg = 'project_id'
    serializer_class = StepSerializer

    def retrieve(self, request, *args, **kwargs):
        target_project = self.get_object()
        if not len(target_project.steps.all()):
            return Response(status=status.HTTP_204_NO_CONTENT)
        for step in target_project.steps.all().order_by('number'):
            if step.status != 'Completed':
                serializer = self.get_serializer(step)
                return Response(serializer.data)
        return Response(status=status.HTTP_204_NO_CONTENT)


class UpdateStepSetStepAsCompleted(UpdateAPIView):
    """
    Update a specified step and set it as completed, updating the group organization
    and setting the chart's histories as no longer pending
    """
    queryset = Step.objects.all()
    lookup_url_kwarg = 'step_id'
    serializer_class = StepSerializer

    def perform_update(self, serializer):
        # Update all info of the step
        target_step = self.get_object()
        target_step.description = serializer.validated_data.get('description')
        target_step.effective_data = serializer.validated_data.get('effective_date')
        target_step.number = serializer.validated_data.get('number')
        target_step.status = serializer.validated_data.get('status')
        target_step.save()
        # Update all Entities in the Group
        target_chart = Chart.objects.get(step=target_step)
        list_of_entities = json.loads(target_chart.nodes)
        for entity in list_of_entities:
            try:
                # Update the entity for any info that was changed in the step
                target_entity = Entity.objects.get(id=entity['id'])
                target_entity.pid = entity['pid']
                target_entity.name = entity['name']
                target_entity.legal_form = entity['legal_form']
                target_entity.location = entity['location']
                if 'tax_rate' in entity:
                    target_entity.tax_rate = entity['tax_rate']
                # Toggle the active status of the entity so it becomes an official part of the group organization
                if 'new' in entity:
                    target_entity.active = True
                target_entity.save()
            except Entity.DoesNotExist:
                # Handle when it is an entity only for Delete Highlighting in the front, no backend data exists
                pass
        # Set all Charts histories as pending = False
        list_of_histories = EntityHistory.objects.filter(chart=target_chart)
        for history in list_of_histories:
            history.pending = False
            history.save()
        return Response(status=status.HTTP_200_OK)
