from rest_framework import serializers
from .models import Feedback
from ..users.serializers import UserSerializer


class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = ['title', 'content']
