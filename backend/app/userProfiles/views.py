from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.generics import RetrieveUpdateAPIView, ListAPIView, CreateAPIView
from rest_framework.response import Response
from app.projectRoles.models import ProjectRole
from app.projects.models import Project
from app.tasks.serializers import TaskSerializer
from app.users.serializers import UpdateUserSerializer

User = get_user_model()


class RetrieveUpdateLoggedInUserProfile(RetrieveUpdateAPIView):
    """
    get:
    Retrieve the logged in User's Profile

    update:
    Update the logged in User's Profile
    """
    serializer_class = UpdateUserSerializer
    permission_classes = []

    def get_object(self):
        return self.request.user.user_profile

    def patch(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = {
            **serializer.validated_data
        }
        user_profile = self.get_object()
        user_profile.phone_number = request.data['phone_number']
        user_profile.user.email = validated_data['email']
        user_profile.user.username = validated_data['username']
        user_profile.user.first_name = validated_data['first_name']
        user_profile.user.last_name = validated_data['last_name']
        user_profile.save()
        user_profile.user.save()
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
        # IF user already has a ProjectRole for Project
        for project_role in all_assigned_roles:
            if project_role.user == target_user_profile:
                # Update the Project Role with the new requst.data["role"]
                project_role.role = request.data['role']
                return Response(status=status.HTTP_200_OK)
        # ELSE
        # Create the Project Role that connects the User to the Project
        new_project_role = ProjectRole(
            # Assign its role to be request.data["role"]
            role=request.data['role'],
            user=target_user_profile,
            project=target_project
        )
        new_project_role.save()
        # Add the role to Project.assigned_users_roles
        target_project.assigned_users_roles.add(new_project_role)
        # Add the role to UserProfile.assigned_project_roles
        target_user_profile.assigned_project_roles.add(new_project_role)
        return Response(status=status.HTTP_200_OK)
