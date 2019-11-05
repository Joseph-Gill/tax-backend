from django.contrib.auth import get_user_model
from django.dispatch import receiver
from rest_framework import serializers
from app.registration.signals import post_user_registration_validation
from app.social.models.profile import SocialProfile

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """
    UserSerializer
    """

    class Meta:
        model = User
        fields = ['id', 'username', 'email']


class SocialProfileSerializer(serializers.ModelSerializer):
    logged_in_user_is_following = serializers.SerializerMethodField()
    user = UserSerializer(read_only=True, many=False)

    def get_logged_in_user_is_following(self, social_profile):
        return social_profile in self.context['request'].social_profile.followees.all()

    class Meta:
        model = SocialProfile
        fields = ['id', 'avatar', 'location', 'about_me', 'job', 'followees', 'followers',
                  'logged_in_user_is_following', 'user']


@receiver(post_user_registration_validation)
def create_social_profile(sender, user, **kwargs):
    SocialProfile(user=user).save()
