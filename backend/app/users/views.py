from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.generics import ListAPIView, RetrieveAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from app.groups.models import Group
from app.userProfiles.serializers import UserProfileSerializer
from app.users.serializers import UserSerializer
from django.contrib.auth.hashers import check_password

User = get_user_model()


class ListUsers(ListAPIView):
    """
    List all Users.
    """
    serializer_class = UserSerializer
    queryset = User.objects.all()


class RetrieveUser(RetrieveAPIView):
    """
    Retrieve one User.
    """
    serializer_class = UserSerializer
    queryset = User.objects.all()
    lookup_url_kwarg = 'user_id'


class RetrieveUpdateDestroyLoggedInUser(RetrieveUpdateDestroyAPIView):
    """
    get:
    Retrieve logged-in User.

    update:
    Update User.

    delete:
    Delete logged-in User.
    """
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def get_object(self):
        return self.request.user

    def destroy(self, request, *args, **kwargs):
        target_user = self.get_object()
        current_password = target_user.password
        match = check_password(request.data['password'], current_password)
        if match:
            self.perform_destroy(target_user)
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_204_NO_CONTENT)


class RetrieveAllUsersForSpecificGroup(ListAPIView):
    """
    Retrieve all Users for a specified Group
    """
    serializer_class = UserProfileSerializer
    queryset = Group
    lookup_url_kwarg = 'group_id'
    permission_classes = []

    def list(self, request, *args, **kwargs):
        target_group = self.get_object()
        serializer = self.get_serializer(target_group.users.all(), many=True)
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
