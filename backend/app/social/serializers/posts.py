from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from app.social.models.comments import Comment
from app.social.models.posts import Post
from app.social.models.profile import SocialProfile

user = get_user_model()


class PostUserSerializer(serializers.ModelSerializer):
    """
    UserSerializer for nested usage in PostSerializer.
    """

    class Meta:
        model = user
        fields = ['id', 'username', 'email']


class SocialProfileSerializer(serializers.ModelSerializer):
    """
    UserSerializer for nested usage in PostSerializer.
    """
    user = PostUserSerializer(read_only=True, many=False)

    class Meta:
        model = SocialProfile
        fields = ["id", "user", "created", "modified", "avatar", "location", "about_me", "job","followees",
                  "liked_posts"]


class CommentSerializer(serializers.ModelSerializer):
    social_profile = SocialProfileSerializer(read_only=True)
    is_from_logged_in_user = SerializerMethodField()

    # logged_in_user_clapped = SerializerMethodField()

    # def get_logged_in_user_clapped(self, comment):
    #     user = self.context['request'].user
    #     if user == comment.user:
    #         return False
    #     if comment in Comment.objects.filter(claps__user=user, post=comment.post):
    #         return True
    #     return False

    def get_is_from_logged_in_user(self, comment):
        user = self.context['request'].user
        if user == comment.user:
            return True
        return False

    class Meta:
        model = Comment
        fields = '__all__'


class PostSerializer(serializers.ModelSerializer):
    social_profile = SocialProfileSerializer(read_only=True)
    # comments = CommentSerializer(many=True, read_only=True)
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
