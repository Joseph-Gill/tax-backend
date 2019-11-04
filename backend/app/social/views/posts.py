from rest_framework.generics import ListAPIView, GenericAPIView, ListCreateAPIView, \
    RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from app.social.models.posts import Post
from app.social.permissions import IsOwnerOrReadOnly, IsNotOwner
from app.social.serializers.posts import PostSerializer
from app.social.views.cutom_mixins import FilterPostMixin, CustomDispatchMixin


class ListCreatePosts(ListCreateAPIView, FilterPostMixin, CustomDispatchMixin):
    """
    get:
    List all Posts.
    post:
    Create a new Post.
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def get_queryset(self):
        posts = Post.objects.all().order_by("-created")
        return self.filter_posts(posts)


class RetrieveUpdateDestroyPost(RetrieveUpdateDestroyAPIView, CustomDispatchMixin):
    """
    get:
    Retrieve Post.

    patch:
    Update Post.

    delete:
    Delete Post.
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]


class ListPostsUser(ListAPIView, CustomDispatchMixin):
    """
    get:
    List al posts of a specific User.
    """
    serializer_class = PostSerializer

    def get_queryset(self):
        user_id = self.kwargs.get("pk")
        return Post.objects.filter(user=user_id).order_by("-created")


class ListPostsFollowees(ListAPIView, FilterPostMixin, CustomDispatchMixin):
    """
    get:
    List all Posts of Users the logged-in User follows.
    """
    serializer_class = PostSerializer

    def get_queryset(self):
        followed_user_ids = self.request.social_profile.followees.all().values_list("id", flat=True)
        posts = Post.objects.filter(user__in=followed_user_ids)
        return self.filter_posts(posts)


class ListPostsLoggedInUser(ListAPIView, FilterPostMixin, CustomDispatchMixin):
    """
    get:
    List all Posts of logged-in User.
    """
    serializer_class = PostSerializer

    def get_queryset(self):
        posts = self.request.social_profile.posts
        return self.filter_posts(posts)


class ListLikes(ListAPIView, FilterPostMixin, CustomDispatchMixin):
    """
    get:
    List all Posts bookmarked by logged-in User.
    """
    serializer_class = PostSerializer

    def get_queryset(self):
        posts = Post.objects.filter(liked_by=self.request.social_profile)
        return self.filter_posts(posts)


class CreateLike(GenericAPIView, CustomDispatchMixin):
    """
    post:
    Like Post for logged-in User.
    """
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    permission_classes = [IsNotOwner]

    def post(self, request, pk):
        post_to_save = self.get_object()
        user = request.social_profile
        if post_to_save in user.liked_posts.all():
            user.liked_posts.remove(post_to_save)
            return Response(self.get_serializer(instance=post_to_save).data)
        user.liked_posts.add(post_to_save)
        return Response(self.get_serializer(instance=post_to_save).data)
