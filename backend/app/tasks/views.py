from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.generics import RetrieveUpdateDestroyAPIView, CreateAPIView, ListAPIView
from rest_framework.response import Response
from app.emails.signals import send_email
from app.steps.models import Step
from app.tasks.models import Task
from app.tasks.serializers import TaskSerializer

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


class CreateTaskForSpecificStepForSpecificUser(CreateAPIView):
    """
    Create a Task for a specified Step and for a specified User
    """
    serializer_class = TaskSerializer

    def create(self, request, *args, **kwargs):
        target_step = Step.objects.filter(id=kwargs['step_id'])[0]
        target_user_profile = User.objects.filter(id=kwargs['user_id'])[0].user_profile
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        new_task = Task(
            **serializer.validated_data,
            assigned_user=target_user_profile
        )
        new_task.save()
        target_step.tasks.add(new_task)
        send_email.send(sender=Task, request=request, to=target_user_profile.user.email, email_type='user_assigned_task')
        return Response(status=status.HTTP_201_CREATED)


class UpdateUserForSpecificTask(CreateAPIView):
    """
    Update User assigned to a specified Task
    """
    permission_classes = []

    def create(self, request, *args, **kwargs):
        target_task = Task.objects.filter(id=kwargs['task_id'])[0]
        target_user_profile = User.objects.filter(id=kwargs['user_id'])[0].user_profile
        target_task.assigned_user = target_user_profile
        target_task.save()
        send_email.send(sender=Task, request=request, to=target_user_profile.user.email, email_type='user_assigned_task')
        return Response(status=status.HTTP_202_ACCEPTED)
