from django.urls import path, include
from app.social.views.comments import CreateComment
from app.social.views.posts import ListCreatePosts, RetrieveUpdateDestroyPost, ListPostsUser, ListPostsLoggedInUser, \
    ListPostsFollowees, ListLikes, CreateLike

post_patterns = [
    path('', ListCreatePosts.as_view(), name='list-create-posts'),
    path('<int:pk>/', RetrieveUpdateDestroyPost.as_view(), name='retrieve-update-destroy-post'),
    path('user/<int:pk>/', ListPostsUser.as_view(), name='list-posts-user'),
    path('me/', ListPostsLoggedInUser.as_view(), name='list-posts-logged-in-user'),
    path("following/", ListPostsFollowees.as_view(), name="list-posts-followees"),
    path("likes/", ListLikes.as_view(), name="list-liked-posts"),
    path("toggle-like/<int:pk>/", CreateLike.as_view(), name="toggle-like"),
]

comment_patterns = [
    path("<int:pk>/", CreateComment.as_view(), name="create-post-comment"),
]

urlpatterns = [
    path('posts/', include(post_patterns)),
    path('comments/', include(comment_patterns))
]