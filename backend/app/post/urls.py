from django.urls import path
from app.post.views import ListCreatePosts, RetrieveUpdateDestroyPost, ListPostsUser, ListPostsFollowees, ListLikes, \
    ListPostsLoggedInUser, CreateLike, CreateComment

urlpatterns = [
    path('', ListCreatePosts.as_view(), name='list-create-posts'),
    path('<int:pk>/', RetrieveUpdateDestroyPost.as_view(), name='retrieve-update-destroy-post'),
    path('user/<int:pk>/', ListPostsUser.as_view(), name='list-posts-user'),
    path('me/', ListPostsLoggedInUser.as_view(), name='list-posts-logged-in-user'),
    path("following/", ListPostsFollowees.as_view(), name="list-posts-followees"),
    path("likes/", ListLikes.as_view(), name="list-liked-posts"),
    path("toggle-like/<int:pk>/", CreateLike.as_view(), name="toggle-like"),
    path("comment/<int:pk>/", CreateComment.as_view(), name="create-post-comment"),
]
