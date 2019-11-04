from rest_framework.generics import ListAPIView, GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from app.social.models.profile import SocialProfile
from app.social.serializers.users import SocialProfileSerializer
from app.social.views.cutom_mixins import CustomDispatchMixin
from app.social.permissions import ObjNotLoggedInUser


class ListFollowers(ListAPIView, CustomDispatchMixin):
    """
    get:
    List all followers of the logged-in User.
    """
    serializer_class = SocialProfileSerializer
    queryset = SocialProfile.objects.all()

    def filter_queryset(self, queryset):
        return self.request.social_profile.followers


class ListFollowing(ListAPIView, CustomDispatchMixin):
    """
    get:
    List all Users the logged-in User is following.
    """
    serializer_class = SocialProfileSerializer
    queryset = SocialProfile.objects.all()

    def filter_queryset(self, queryset):
        return self.request.social_profile.followees


class FollowUnfollowUser(GenericAPIView, CustomDispatchMixin):
    """
    post:
    Toggle following User.
    """
    queryset = SocialProfile.objects.all()
    serializer_class = SocialProfileSerializer
    permission_classes = [IsAuthenticated, ObjNotLoggedInUser]

    def post(self, request, pk):
        target_user = self.get_object()
        profile = request.social_profile
        if target_user in profile.followees.all():
            profile.followees.remove(target_user)
            return Response(self.get_serializer(instance=target_user).data)
        profile.followees.add(target_user)
        return Response(self.get_serializer(instance=target_user).data)
