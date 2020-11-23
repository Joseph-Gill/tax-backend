from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView
from rest_framework import status
from app.groups.models import Group
from app.groups.serializers import GroupSerializer
from rest_framework.response import Response


class ListAllOrCreateGroup(ListCreateAPIView):
    """
    get:
    List all Groups

    post:
    Create a new Group
    """
    serializer_class = GroupSerializer
    queryset = Group.objects.all()


class ListAllUsersGroups(ListAPIView):
    """
    List all Groups of logged in User
    """
    serializer_class = GroupSerializer

    def list(self, request, *args, **kwargs):
        queryset = request.user.user_profile.groups.all()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class RetrieveUpdateDestroySpecificGroup(RetrieveUpdateDestroyAPIView):
    """
    get:
    List a specified Group

    update:
    Update a specified Group

    delete:
    Delete a specified Group
    """
    pass
