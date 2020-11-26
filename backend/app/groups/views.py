from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView, CreateAPIView
from rest_framework import status
from app.groups.models import Group
from app.groups.serializers import GroupSerializer
from rest_framework.response import Response
from app.groups.signals import post_user_group_creation
from app.registration.serializers import RegistrationSerializer
from app.userProfiles.models import UserProfile
from django.contrib.auth import get_user_model

User = get_user_model()


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
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        new_group = Group(
            **serializer.validated_data
        )
        new_group.save()
        users_profile.groups.add(new_group)
        post_user_group_creation.send(sender=Group, user_profile=users_profile, name=request.data['name'], new_group=new_group)
        return Response(status=status.HTTP_201_CREATED)


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


class AddRemoveUserInSpecificGroup(CreateAPIView):
    """
    Toggle a specified User being a member of a specified Group
    """
    serializer_class = RegistrationSerializer
    permission_classes = []

    def create(self, request, *args, **kwargs):
        target_user = User.objects.filter(email=request.data["email"])
        target_group = Group.objects.filter(id=kwargs['group_id'])[0]
        if target_user:
            target_user_profile = target_user[0].user_profile
            if target_group in target_user_profile.groups.all():
                target_user_profile.groups.remove(target_group)
            else:
                target_user_profile.groups.add(target_group)
                # Need to remove User's Registration Profile from Group.invited_new_users if it exists there
                # Need to add sending them an email here
            return Response(status=status.HTTP_202_ACCEPTED)
        else:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(serializer.validated_data)
            # Need to add the newly created Registration Profile to Group.invited_new_users
            return Response(status=status.HTTP_200_OK)
