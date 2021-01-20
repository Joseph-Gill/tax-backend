from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView
from rest_framework.response import Response
from app.groups.models import Group
from app.projects.models import Project
from app.projects.serializers import ProjectSerializer
from app.projects.signals import post_user_project_creation
from app.userProfiles.models import UserProfile
from app.userProfiles.serializers import UserProfileSerializer


class ListAllOrCreateProjectForSpecificGroup(ListCreateAPIView):
    """
    get:
    List all Projects for a specified Group

    post:
    Create a new Project for a specified Group
    """
    queryset = Group
    serializer_class = ProjectSerializer
    lookup_url_kwarg = 'group_id'
    permission_classes = []

    def list(self, request, *args, **kwargs):
        target_group = self.get_object()
        projects = target_group.projects.all().order_by('created')
        serializer = self.get_serializer(projects, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        users_profile = UserProfile.objects.get(user=request.user)
        target_group = self.get_object()
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        new_project = Project(
            **serializer.validated_data
        )
        new_project.save()
        target_group.projects.add(new_project)
        post_user_project_creation.send(sender=Project, user_profile=users_profile, new_project=new_project)
        return Response(status=status.HTTP_201_CREATED)


class RetrieveUpdateDestroySpecificProject(RetrieveUpdateDestroyAPIView):
    """
    get:
    List a specified Project

    update:
    Update a specified Project

    delete:
    Delete a specified Project
    """
    http_method_names = ['get', 'patch', 'delete']
    serializer_class = ProjectSerializer
    queryset = Project.objects.all()
    lookup_url_kwarg = 'project_id'


class ListUsersWithAccessToProject(ListAPIView):
    """
    List all User Profiles with access to a specified Project
    """
    serializer_class = UserProfileSerializer
    queryset = Project.objects.all()
    lookup_url_kwarg = 'project_id'

    def list(self, request, *args, **kwargs):
        target_project = self.get_object()
        target_user_profiles = UserProfile.objects.filter(assigned_project_roles__project=target_project)
        serializer = self.get_serializer(target_user_profiles, many=True)
        return Response(serializer.data)
