from rest_framework.generics import ListAPIView, RetrieveAPIView, RetrieveUpdateDestroyAPIView

from app.social.models import SocialProfile
from app.social.serializers.users import SocialProfileSerializer
from app.social.views.cutom_mixins import CustomDispatchMixin


class ListSocialProfiles(ListAPIView, CustomDispatchMixin):
    """
    List all Social Profiles.
    """
    serializer_class = SocialProfileSerializer
    queryset = SocialProfile.objects.all()


class RetrieveSocialProfiles(RetrieveAPIView, CustomDispatchMixin):
    """
    Retrieve one Social Profile.
    """
    serializer_class = SocialProfileSerializer
    queryset = SocialProfile.objects.all()
    lookup_url_kwarg = 'social_profile_id'


class RetrieveUpdateDestroyLoggedInUserSocialProfiles(RetrieveUpdateDestroyAPIView, CustomDispatchMixin):
    """
    get:
    Retrieve logged-in User Social Profile.

    update:
    Update User.

    delete:
    Delete logged-in User Social Profile.
    """
    serializer_class = SocialProfileSerializer
    queryset = SocialProfile.objects.all()

    def get_object(self):
        return self.request.social_profile
