from django.contrib.auth import get_user_model
from django.dispatch import receiver
from rest_framework import serializers

from app.registration.signals import post_user_registration_validation
from app.social.models.profile import SocialProfile
from app.social.serializers.posts import PostSerializer

User = get_user_model()


class SocialProfileSerializer(serializers.ModelSerializer):
    post_count = serializers.SerializerMethodField()
    logged_in_user_is_following = serializers.SerializerMethodField()
    posts = PostSerializer(many=True, read_only=True)

    def get_post_count(self, social_profile):
        return social_profile.liked_posts.count()

    def get_logged_in_user_is_following(self, social_profile):
        return social_profile in self.context['request'].social_profile.followees.all()

    class Meta:
        model = SocialProfile
        fields = ['id', 'avatar', 'location', 'about_me', 'job',
                  'post_count', 'followees', 'followers',
                  'logged_in_user_is_following', 'posts']


@receiver(post_user_registration_validation)
def create_social_profile(sender, user, **kwargs):
    SocialProfile(user=user).save()
