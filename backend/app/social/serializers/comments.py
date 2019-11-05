from rest_framework import serializers
from rest_framework.fields import SerializerMethodField
from app.social.models.comments import Comment
from app.social.serializers.users import SocialProfileSerializer


class CommentSerializer(serializers.ModelSerializer):
    social_profile = SocialProfileSerializer(read_only=True)
    is_from_logged_in_user = SerializerMethodField()

    def get_is_from_logged_in_user(self, comment):
        social_profile = self.context['request'].social_profile
        if social_profile == comment.social_profile:
            return True
        return False

    class Meta:
        model = Comment
        fields = '__all__'
