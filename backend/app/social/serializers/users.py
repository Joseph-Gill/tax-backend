from django.contrib.auth import get_user_model
from rest_framework import serializers
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
    logged_in_user_is_friends = serializers.SerializerMethodField()
    user = UserSerializer(read_only=True, many=False)

    def get_logged_in_user_is_following(self, social_profile):
        return social_profile in self.context['request'].social_profile.followees.all()

    def get_logged_in_user_is_friends(self, social_profile):
        return social_profile in self.context['request'].social_profile.friends

    class Meta:
        model = SocialProfile
        fields = ['id', 'avatar', 'location', 'about_me', 'job', 'followees', 'followers',
                  'logged_in_user_is_following', 'logged_in_user_is_friends', 'user']
