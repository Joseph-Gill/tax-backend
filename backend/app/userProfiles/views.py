from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.generics import RetrieveUpdateAPIView, ListAPIView, CreateAPIView, RetrieveAPIView
from rest_framework.response import Response

from app.groups.models import Group
from app.organizations.models import Organization
from app.projectRoles.models import ProjectRole
from app.projects.models import Project
from app.tasks.serializers import TaskSerializer
from app.userProfiles.models import UserProfile
from app.userProfiles.serializers import UpdateUserProfileSerializer, UserProfileSerializer
import json

User = get_user_model()


class RetrieveUpdateLoggedInUserProfile(RetrieveUpdateAPIView):
    """
    get:
    Retrieve the logged in User's Profile

    update:
    Update the logged in User's Profile
    """
    permission_classes = []
    serializer_class = UpdateUserProfileSerializer

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return UserProfileSerializer

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
        group_project_statuses = request.data['member_project_access']
        target_user_profile = UserProfile.objects.get(id=kwargs['userprofile_id'])
        user_project_roles = ProjectRole.objects.filter(user__id=kwargs['userprofile_id'], project__group__id=kwargs['group_id'])
        current_role = request.data['role']
        current_org = Organization.objects.get(id=request.data['organization']['id'])
        previous_user_org_for_group = Organization.objects.filter(user_profiles__id=kwargs['userprofile_id'], group__id=kwargs['group_id'])
        if len(previous_user_org_for_group):
            for org in previous_user_org_for_group:
                org.user_profiles.remove(target_user_profile)
        target_user_profile.organizations.add(current_org)
        for project in group_project_statuses:
            filtered_role = list(filter(lambda role: (role.project.id == project['id']), user_project_roles))
            if len(filtered_role):
                if not filtered_role[0].role == current_role:
                    filtered_role[0].role = current_role
                    filtered_role[0].save()
                if not project['access']:
                    filtered_role[0].delete()
            else:
                if project['access']:
                    target_project = Project.objects.get(id=project['id'])
                    target_user_profile = UserProfile.objects.get(id=kwargs['userprofile_id'])
                    new_project_role = ProjectRole(
                        role=current_role,
                    )
                    new_project_role.save()
                    target_user_profile.assigned_project_roles.add(new_project_role)
                    target_project.assigned_users_roles.add(new_project_role)
        return Response(status=status.HTTP_202_ACCEPTED)


class RetrieveSpecificUser(RetrieveAPIView):
    """
    Get a specified User's information
    """
    serializer_class = UserProfileSerializer
    permission_classes = []
    queryset = UserProfile.objects.all()
    lookup_url_kwarg = 'userprofile_id'
