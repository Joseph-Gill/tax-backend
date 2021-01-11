from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.generics import RetrieveUpdateDestroyAPIView, CreateAPIView, ListAPIView, RetrieveAPIView
from rest_framework.response import Response
from app.emails.signals import send_email
from app.projects.models import Project
from app.steps.models import Step
from app.taskDocuments.models import TaskDocument
from app.tasks.models import Task
from app.tasks.serializers import TaskSerializer
from app.userProfiles.models import UserProfile
import json

User = get_user_model()


class ListAllTasksForSpecificStep(ListAPIView):
    """
    List all Tasks for a specified Step
    """
    queryset = Step
    serializer_class = TaskSerializer
    lookup_url_kwarg = 'step_id'
    permission_classes = []

    def list(self, request, *args, **kwargs):
        target_step = self.get_object()
        tasks = target_step.tasks.all().order_by('due_date')
        serializer = self.get_serializer(tasks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class RetrieveUpdateDestroySpecificTask(RetrieveUpdateDestroyAPIView):
    """
    get:
    List a specified Task

    update:
    Update a specified Task

    delete:
    Delete a specified Task
    """
    http_method_names = ['get', 'patch', 'delete']
    serializer_class = TaskSerializer
    queryset = Task.objects.all()
    lookup_url_kwarg = 'task_id'

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        target_task = self.get_object()
        serializer = self.get_serializer(target_task, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        target_userprofile = UserProfile.objects.get(id=request.data['assigned_user_profile'])
        target_step = Step.objects.get(id=request.data['task_step'])
        target_task.step = target_step
        target_task.assigned_user = target_userprofile
        target_task.save()
        for task_document in request.FILES:
            new_task_document = TaskDocument(
                name=request.FILES[task_document].name,
                document=request.FILES[task_document],
                task=target_task
            )
            new_task_document.save()
        self.perform_update(serializer)
        return Response(serializer.data)


class CreateTaskForSpecificStepForSpecificUser(CreateAPIView):
    """
    Create a Task for a specified Step and for a specified User
    """
    serializer_class = TaskSerializer

    def create(self, request, *args, **kwargs):
        target_step = Step.objects.filter(id=kwargs['step_id'])[0]
        target_user_profile = UserProfile.objects.get(id=kwargs['userprofile_id'])
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        new_task = Task(
            **serializer.validated_data,
            assigned_user=target_user_profile
        )
        new_task.save()
        for task_document in request.FILES:
            new_task_document = TaskDocument(
                name=request.FILES[task_document].name,
                document=request.FILES[task_document],
                task=new_task
            )
            new_task_document.save()
        target_step.tasks.add(new_task)
        send_email.send(sender=Task, request=request, to=target_user_profile.user.email, email_type='user_assigned_task')
        return Response(status=status.HTTP_201_CREATED)


class UpdateUserForSpecificTask(CreateAPIView):
    """
    Update User assigned to a specified Task
    """
    permission_classes = []

    def create(self, request, *args, **kwargs):
        target_task = Task.objects.get(id=kwargs['task_id'])
        target_user_profile = User.objects.get(id=kwargs['user_id']).user_profile
        target_task.assigned_user = target_user_profile
        target_task.save()
        send_email.send(sender=Task, request=request, to=target_user_profile.user.email, email_type='user_assigned_task')
        return Response(status=status.HTTP_202_ACCEPTED)


class ListAllTasksForSpecifiedProject(ListAPIView):
    """
    Get all tasks for a specified Project
    """
    serializer_class = TaskSerializer
    queryset = Project.objects.all()
    lookup_url_kwarg = 'project_id'

    def list(self, request, *args, **kwargs):
        target_project = self.get_object()
        tasks = list(Task.objects.filter(step__project__id=target_project.id))
        tasks.sort(key=lambda x: (x.step.number, x.created))
        serializer = self.get_serializer(tasks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ListAllTasksForSpecifiedStepOfProject(ListAPIView):
    """
    Get all tasks for a specified Step of a specified Project
    """

    serializer_class = TaskSerializer
    queryset = Project.objects.all()
    lookup_url_kwarg = 'project_id'

    def list(self, request, *args, **kwargs):
        target_project = self.get_object()
        tasks = list(Task.objects.filter(step__project__id=target_project.id, step__number=kwargs['step_number']))
        tasks.sort(key=lambda x: x.created)
        serializer = self.get_serializer(tasks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class RetrieveProjectTasksStatusNumbers(RetrieveAPIView):
    """
    Retrieve status numbers for all Tasks of a specified Project
    """
    queryset = Project.objects.all()
    lookup_url_kwarg = 'project_id'

    def retrieve(self, request, *args, **kwargs):
        target_project = self.get_object()
        task_status_results = {
            "Ongoing": 0,
            "Planned": 0,
            "Completed": 0,
            "Not Started": 0
        }
        target_tasks = Task.objects.filter(step__project__id=target_project.id)
        for task in target_tasks:
            task_status_results[task.status] = task_status_results[task.status] + 1
        return Response(task_status_results, status=status.HTTP_200_OK)