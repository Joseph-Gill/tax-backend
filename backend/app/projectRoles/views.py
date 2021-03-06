from rest_framework.generics import RetrieveAPIView, CreateAPIView
from rest_framework.response import Response
from app.groups.models import Group
from app.projectRoles.models import ProjectRole
from app.projectRoles.serializers import ProjectRoleSerializer
from app.projects.models import Project
from app.userProfiles.models import UserProfile


class ListRolesForSpecifiedUserProfileGroup(RetrieveAPIView):
    """
    List all Roles for a specified UserProfile of specified Group
    """
    serializer_class = ProjectRoleSerializer
    queryset = ProjectRole

    def retrieve(self, request, *args, **kwargs):
        target_user_profile = UserProfile.objects.get(id=kwargs['userprofile_id'])
        target_group = Group.objects.get(id=kwargs['group_id'])
        instance = ProjectRole.objects.filter(user_id=target_user_profile.id, project__group_id=target_group.id)
        serializer = self.get_serializer(instance, many=True)
        return Response(serializer.data)


class ListAllUsersWithRoleForSpecifiedProject(RetrieveAPIView):
    """
    List all user roles for a specified Project of a specified Group
    """
    serializer_class = ProjectRoleSerializer
    queryset = ProjectRole

    def retrieve(self, request, *args, **kwargs):
        target_group = Group.objects.get(id=kwargs['group_id'])
        target_project = Project.objects.get(id=kwargs['project_id'])
        instance = ProjectRole.objects.filter(user__groups__id=target_group.id, project__id=target_project.id)
        serializer = self.get_serializer(instance, many=True)
        return Response(serializer.data)


class ToggleUserFavoriteProjectStatus(CreateAPIView):
    """
    Toggle favorite status for a specific Project for logged in User
    """
    serializer_class = ProjectRoleSerializer

    def post(self, request, *args, **kwargs):
        target_project_role = ProjectRole.objects.get(user_id=kwargs['userprofile_id'], project_id=kwargs['project_id'])
        target_project_role.favorite = not target_project_role.favorite
        target_project_role.save()
        serializer = self.get_serializer(target_project_role)
        return Response(serializer.data)
