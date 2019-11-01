from django.urls import path
from app.post.views import ListCreatePosts, RetrieveUpdateDestroyPost, ListPostsUser, ListPostsFollowees, ListBookmarks, \
    ListPostsLoggedInUser, CreateBookmark, CreateDestroyClapPost, CreateComment, CreateDestroyCommentClap

urlpatterns = [
    path('', ListCreatePosts.as_view(), name='list-create-posts'),
    path('<int:pk>/', RetrieveUpdateDestroyPost.as_view(), name='retrieve-update-destroy-post'),
    path('user/<int:pk>/', ListPostsUser.as_view(), name='list-posts-user'),
    path('me/', ListPostsLoggedInUser.as_view(), name='list-posts-logged-in-user'),
    path("following/", ListPostsFollowees.as_view(), name="list-posts-followees"),
    path("bookmarked/", ListBookmarks.as_view(), name="list-bookmarked-posts"),
    path("bookmark/<int:pk>/", CreateBookmark.as_view(), name="create-bookmark"),
    path("clap/<int:pk>/", CreateDestroyClapPost.as_view(), name="create-destroy-clap-post"),
    path("comment/<int:pk>/", CreateComment.as_view(), name="create-post-comment"),
    path("comment/clap/<int:comment_id>/", CreateDestroyCommentClap.as_view(), name="create-destroy-comment-clap"),
]
