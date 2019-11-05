from rest_framework.generics import CreateAPIView

from app.social.models.friends import Friend


class CreateFriendRequest(CreateAPIView):
    queryset = Friend.objects.all
