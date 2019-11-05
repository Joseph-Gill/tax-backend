from rest_framework import serializers

from app.social.models import Friend
from app.social.serializers.users import SocialProfileSerializer


class FriendSerializer(serializers.ModelSerializer):
    requester = SocialProfileSerializer()
    receiver = SocialProfileSerializer()

    class Meta:
        model = Friend
        fields = ['id', 'requester', 'receiver', 'status', 'created']
