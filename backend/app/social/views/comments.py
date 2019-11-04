from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from app.social.models.comments import Comment
from app.social.models.posts import Post
from app.social.serializers.posts import PostSerializer


class CreateComment(GenericAPIView):
    """
    post:
    Create a new Comment.
    """
    serializer_class = PostSerializer
    queryset = Post.objects.all()

    def post(self, request, pk):
        post = self.get_object()
        comment = Comment(user=request.user, post=post, comment=request.data['comment'])
        comment.save()
        return Response(self.get_serializer(instance=post).data)
