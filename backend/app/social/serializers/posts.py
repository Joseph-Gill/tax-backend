from rest_framework import serializers
from rest_framework.fields import SerializerMethodField
from app.social.models.posts import Post
from app.social.serializers.users import SocialProfileSerializer


class PostSerializer(serializers.ModelSerializer):
    social_profile = SocialProfileSerializer(read_only=True)
    logged_in_user_liked = SerializerMethodField()
    is_from_logged_in_user = SerializerMethodField()

    def get_is_from_logged_in_user(self, post):
        user = self.context['request'].user
        if user == post.social_profile:
            return True
        return False

    def get_logged_in_user_liked(self, post):
        social_profile = self.context['request'].social_profile
        if post in social_profile.liked_posts.all():
            return True
        return False

    class Meta:
        model = Post
        fields = '__all__'

    def create(self, validated_data):
        validated_data['social_profile'] = self.context['request'].social_profile
        post = super().create(validated_data=validated_data)
        return post
