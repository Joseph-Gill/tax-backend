from rest_framework.generics import ListAPIView, GenericAPIView, ListCreateAPIView, \
    RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from app.post.models import Post, ClapPost, Comment, ClapComment
from app.post.permissions import IsOwnerOrReadOnly, IsNotOwner
from app.post.serializers import PostSerializer, CommentSerializer


class FilterPostMixin:
    def filter_posts(self, posts):
        if "search" in self.request.query_params.keys():
            posts_including_search = []
            search = self.request.query_params["search"].lower()
            for item in posts:
                if item.user and (search in item.content.lower() or search in item.user.username.lower()):
                    posts_including_search.append(item)
            return posts_including_search
        if "category" in self.request.query_params.keys():
            posts_including_categories = []
            category = self.request.query_params["category"]
            for i in posts:
                if category in i.category:
                    posts_including_categories.append(i)
            return posts_including_categories
        return posts.order_by("-created")


class ListCreatePosts(ListCreateAPIView, FilterPostMixin):
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


class RetrieveUpdateDestroyPost(RetrieveUpdateDestroyAPIView):
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


class ListPostsUser(ListAPIView):
    """
    get:
    List al posts of a specific User.
    """
    serializer_class = PostSerializer

    def get_queryset(self):
        user_id = self.kwargs.get("pk")
        return Post.objects.filter(user=user_id).order_by("-created")


class ListPostsFollowees(ListAPIView, FilterPostMixin):
    """
    get:
    List all Posts of Users the logged-in User follows.
    """
    serializer_class = PostSerializer

    def get_queryset(self):
        followed_user_ids = self.request.user.followees.all().values_list("id", flat=True)
        posts = Post.objects.filter(user__in=followed_user_ids)
        return self.filter_posts(posts)


class ListPostsLoggedInUser(ListAPIView, FilterPostMixin):
    """
    get:
    List all Posts of logged-in User.
    """
    serializer_class = PostSerializer

    def get_queryset(self):
        posts = self.request.user.posts
        return self.filter_posts(posts)


class ListBookmarks(ListAPIView, FilterPostMixin):
    """
    get:
    List all Posts bookmarked by logged-in User.
    """
    serializer_class = PostSerializer

    def get_queryset(self):
        posts = Post.objects.filter(bookmarked_by=self.request.user)
        return self.filter_posts(posts)


class CreateBookmark(GenericAPIView):
    """
    post:
    Bookmark Post for logged-in User.
    """
    serializer_class = PostSerializer
    queryset = Post.objects.all()

    def post(self, request, **kwargs):
        post_to_save = self.get_object()
        user = self.request.user
        if post_to_save in user.bookmarked_posts.all():
            user.bookmarked_posts.remove(post_to_save)
            return Response(self.get_serializer(instance=post_to_save).data)
        user.bookmarked_posts.add(post_to_save)
        return Response(self.get_serializer(instance=post_to_save).data)


class CreateDestroyClapPost(GenericAPIView):
    """
    post:
    Toggle clap Post.
    """
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    permission_classes = [IsAuthenticated, IsNotOwner]

    def post(self, request, pk, **kwargs):
        post = self.get_object()
        clap_post, created = ClapPost.objects.get_or_create(post=post, user=request.user)
        if not created:
            clap_post.delete()
        return Response(self.get_serializer(instance=post).data, status=200)


class CreateComment(GenericAPIView):
    """
    post:
    Create a new Comment.
    """
    serializer_class = PostSerializer
    queryset = Post.objects.all()

    def post(self, request, pk, **kwargs):
        post = self.get_object()
        comment = Comment(user=request.user, post=post, comment=request.data['comment'])
        comment.save()
        return Response(self.get_serializer(instance=post).data)


class CreateDestroyCommentClap(GenericAPIView):
    """
    post:
    Toggle clap Comment.
    """
    serializer_class = PostSerializer
    queryset = Comment.objects.all()
    lookup_url_kwarg = 'comment_id'
    permission_classes = [IsAuthenticated, IsNotOwner]

    def post(self, request, comment_id, **kwargs):
        comment = self.get_object()
        clap, created = ClapComment.objects.get_or_create(user=request.user, comment=comment)
        if not created:
            clap.delete()
        return Response(self.get_serializer(comment.post).data)
