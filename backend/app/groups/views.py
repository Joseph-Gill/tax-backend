from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView

from app.groups.models import Group
from app.groups.serializers import GroupSerializer


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
    pass


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
