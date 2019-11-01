from django.contrib.auth import get_user_model
from rest_framework.generics import ListAPIView, RetrieveAPIView, GenericAPIView, RetrieveUpdateAPIView, \
    RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from app.users.permissions import ObjNotLoggedInUser
from app.users.serializers import UserSerializer

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


class ListFollowers(ListAPIView):
    """
    get:
    List all followers of the logged-in User.
    """
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def filter_queryset(self, queryset):
        return self.request.user.followers


class ListFollowing(ListAPIView):
    """
    get:
    List all Users the logged-in User is following.
    """
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def filter_queryset(self, queryset):
        return self.request.user.followees


class FollowUnfollowUser(GenericAPIView):
    """
    post:
    Toggle following User.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, ObjNotLoggedInUser]

    def post(self, request, pk):
        target_user = self.get_object()
        user = request.user
        if target_user in user.followees.all():
            user.followees.remove(target_user)
            return Response(self.get_serializer(instance=target_user).data)
        user.followees.add(target_user)
        return Response(self.get_serializer(instance=target_user).data)
