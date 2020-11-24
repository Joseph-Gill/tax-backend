from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView, CreateAPIView
from rest_framework import status
from app.groups.models import Group
from app.groups.serializers import GroupSerializer
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from app.userProfiles.models import UserProfile


class ListAllOrCreateGroup(ListCreateAPIView):
    """
    get:
    List all Groups

    post:
    Create a new Group
    """
    permission_classes = []
    serializer_class = GroupSerializer
    queryset = Group.objects.all()

    def create(self, request, *args, **kwargs):
        users_profile = UserProfile.objects.get(user=request.user)
        new_group = Group(
            name=request.data['name']
        )
        new_group.save()
        users_profile.groups.add(new_group)
        users_profile.save()
        return Response(status=status.HTTP_200_OK)


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
    http_method_names = ['get', 'patch', 'delete']
    serializer_class = GroupSerializer
    queryset = Group.objects.all()
    lookup_url_kwarg = 'group_id'


class ToggleUserMembershipInSpecificGroup(CreateAPIView):
    """
    Toggle a specified User being a member of a specified Group
    """
    permission_classes = []
    serializer_class = GroupSerializer
    queryset = Group.objects.all()

    def get_object(self):
        queryset = self.get_queryset()
        filter = {}
        for field in self.multiple_lookup_fields:
            filter[field] = self.kwargs[field]
        obj = get_object_or_404(queryset, **filter)
        self.check_object_permissions(self.request, obj)
        return obj

