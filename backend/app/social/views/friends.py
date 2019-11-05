from django.db.models import Q
from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from app.social.models import SocialProfile, Friend
from app.social.permissions import ObjNotLoggedInUser, FriendRequestDoesNotExist, IsPendingToAllowUpdate
from app.social.serializers.friends import FriendSerializer
from app.social.serializers.users import SocialProfileSerializer
from app.social.views.cutom_mixins import CustomDispatchMixin


class CreateFriendRequest(CreateAPIView, CustomDispatchMixin):
    """
    post:
    Create a new pending friend request.
    """
    queryset = SocialProfile.objects.all()
    serializer_class = FriendSerializer
    lookup_url_kwarg = 'social_profile_id'
    permission_classes = [IsAuthenticated, ObjNotLoggedInUser, FriendRequestDoesNotExist]

    def create(self, request, *args, **kwargs):
        receiver = self.get_object()
        requester = request.social_profile
        friendship = Friend(requester=requester, receiver=receiver)
        friendship.save()
        return Response(self.get_serializer(instance=friendship).data)


class RetrieveUpdateDestroyFriendRequest(RetrieveUpdateDestroyAPIView, CustomDispatchMixin):
    """
    get:
    Retrieve a friend request
    patch:
    Update the status of a friend request
    delete:
    Delete a friend request.
    Only allowed if logged-in user is part of the friendship, as specified in IsPendingToAllowUpdate
    """
    queryset = Friend.objects.all()
    serializer_class = FriendSerializer
    lookup_url_kwarg = 'friend_request_id'
    permission_classes = [IsAuthenticated, IsPendingToAllowUpdate]


class ListFriends(ListAPIView, CustomDispatchMixin):
    """
    get:
    List all social profiles of logged-in users accepted friends.
    """
    serializer_class = SocialProfileSerializer
    queryset = SocialProfile.objects.all()

    def filter_queryset(self, queryset):
        return self.request.social_profile.friends


class ListFriendRequests(ListAPIView, CustomDispatchMixin):
    """
    get:
    List all friend requests in which the logged-in user is involved.
    """
    serializer_class = FriendSerializer
    queryset = Friend.objects.all()

    def filter_queryset(self, queryset):
        requests = Friend.objects.filter(
            Q(receiver=self.request.social_profile) | Q(requester=self.request.social_profile)
        ).distinct()
        if "status" in self.request.query_params.keys():
            status = self.request.query_params["status"].lower()
            return requests.filter(status=status)
        return requests
