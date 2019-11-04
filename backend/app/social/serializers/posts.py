from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from app.social.models.comments import Comment
from app.social.models.posts import Post

user = get_user_model()


class PostUserSerializer(serializers.ModelSerializer):
    """
    UserSerializer for nested usage in PostSerializer.
    """

    class Meta:
        model = user
        fields = ['id', 'username', 'email', 'avatar']


class CommentSerializer(serializers.ModelSerializer):
    user = PostUserSerializer(read_only=True)
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
    user = PostUserSerializer(read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    logged_in_user_liked = SerializerMethodField()
    is_from_logged_in_user = SerializerMethodField()

    def get_is_from_logged_in_user(self, post):
        user = self.context['request'].user
        if user == post.user:
            return True
        return False

    def get_logged_in_user_liked(self, post):
        user = self.context['request'].user
        if post in user.liked_posts.all():
            return True
        return False

    class Meta:
        model = Post
        fields = '__all__'

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        post = super().create(validated_data=validated_data)
        return post
