from django.contrib.auth import get_user_model
from rest_framework import serializers

from app.post.serializers import PostSerializer

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    post_count = serializers.SerializerMethodField()
    logged_in_user_is_following = serializers.SerializerMethodField()
    posts = PostSerializer(many=True, read_only=True)

    def get_post_count(self, user):
        return user.posts.count()

    def get_logged_in_user_is_following(self, user):
        return user in self.context['request'].user.followees.all()

    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'username', 'avatar', 'location', 'about_me', 'job',
                  'post_count', 'followees', 'followers',
                  'logged_in_user_is_following', 'posts']
        read_only_fields = ['email']
