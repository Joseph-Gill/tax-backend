from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.generics import RetrieveUpdateAPIView, ListAPIView, CreateAPIView
from rest_framework.response import Response
from app.projectRoles.models import ProjectRole
from app.projects.models import Project
from app.tasks.serializers import TaskSerializer
from app.userProfiles.serializers import UpdateUserProfileSerializer
from app.users.serializers import UpdateUserSerializer

User = get_user_model()


class RetrieveUpdateLoggedInUserProfile(RetrieveUpdateAPIView):
    """
    get:
    Retrieve the logged in User's Profile

    update:
    Update the logged in User's Profile
    """
    serializer_class = UpdateUserProfileSerializer
    permission_classes = []

    def get_object(self):
        return self.request.user.user_profile

    def patch(self, request, *args, **kwargs):
        user_profile = self.get_object()
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(
            serializer.validated_data,
            user_profile
        )
        return Response(status=status.HTTP_200_OK)


class RetrieveLoggedInUserTasks(ListAPIView):
    """
    List the logged in User's Tasks
    """

    serializer_class = TaskSerializer
    permission_classes = []

    def list(self, request, *args, **kwargs):
        target_user_profile = request.user.user_profile
        serializer = self.get_serializer(target_user_profile.assigned_tasks.all().order_by('due_date'), many=True)
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)


class CreateUpdateSpecificUserSpecificProjectRole(CreateAPIView):
    """
    Create or Update a specified User's Role for a specified Project
    """
    def post(self, request, *args, **kwargs):
        target_user_profile = User.objects.filter(id=kwargs['user_id'])[0].user_profile
        target_project = Project.objects.filter(id=kwargs['project_id'])[0]
        all_assigned_roles = target_project.assigned_users_roles.all()
        for project_role in all_assigned_roles:
            if project_role.user == target_user_profile:
                project_role.role = request.data['role']
                project_role.save()
                return Response(status=status.HTTP_200_OK)
        new_project_role = ProjectRole(
            role=request.data['role'],
            user=target_user_profile,
            project=target_project
        )
        new_project_role.save()
        target_project.assigned_users_roles.add(new_project_role)
        target_user_profile.assigned_project_roles.add(new_project_role)
        return Response(status=status.HTTP_200_OK)
