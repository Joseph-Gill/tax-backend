from django.contrib.auth import get_user_model
from rest_framework import serializers
from app.social.models.profile import SocialProfile

User = get_user_model()


class SocialUserSerializer(serializers.ModelSerializer):
    """
    SocialUserSerializer
    """

    class Meta:
        model = User
        fields = ['id', 'username', 'email']


class SocialProfileSerializer(serializers.ModelSerializer):
    logged_in_user_is_following = serializers.SerializerMethodField()
    logged_in_user_is_friends = serializers.SerializerMethodField()
    user = SocialUserSerializer(read_only=True, many=False)
    avatar = serializers.SerializerMethodField()

    def get_avatar(self, social_profile):
        try:
            upload_url = social_profile.upload_avatar.url
            return self.context['request'].build_absolute_uri(upload_url)
        except ValueError:
            if social_profile.social_avatar:
                return social_profile.social_avatar
            else:
                return ''

    def get_logged_in_user_is_following(self, social_profile):
        return social_profile in self.context['request'].social_profile.followees.all()

    def get_logged_in_user_is_friends(self, social_profile):
        return social_profile in self.context['request'].social_profile.friends

    class Meta:
        model = SocialProfile
        fields = ['id', 'avatar', 'location', 'about_me', 'job', 'followees', 'followers',
                  'logged_in_user_is_following', 'logged_in_user_is_friends', 'user']
