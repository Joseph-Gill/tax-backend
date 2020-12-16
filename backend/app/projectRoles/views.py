from rest_framework.generics import RetrieveAPIView
from rest_framework.response import Response
from app.groups.models import Group
from app.projectRoles.models import ProjectRole
from app.projectRoles.serializers import ProjectRoleSerializer
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
