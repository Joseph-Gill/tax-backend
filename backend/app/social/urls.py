from django.urls import path, include
from app.social.views.comments import ListCreateComment
from app.social.views.followers import ListFollowers, ListFollowing, FollowUnfollowUser
from app.social.views.friends import CreateFriendRequest
from app.social.views.posts import ListCreatePosts, RetrieveUpdateDestroyPost, ListPostsUser, ListPostsLoggedInUser, \
    ListPostsFollowees, ListLikes, CreateLike

post_patterns = [
    path('', ListCreatePosts.as_view(), name='list-create-posts'),
    path('<int:post_id>/', RetrieveUpdateDestroyPost.as_view(), name='retrieve-update-destroy-post'),
    path('profile/<int:social_profile_id>/', ListPostsUser.as_view(), name='list-posts-user'),
    path('me/', ListPostsLoggedInUser.as_view(), name='list-posts-logged-in-user'),
    path("following/", ListPostsFollowees.as_view(), name="list-posts-followees"),
    path("likes/", ListLikes.as_view(), name="list-liked-posts"),
    path("toggle-like/<int:post_id>/", CreateLike.as_view(), name="toggle-like"),
]

comment_patterns = [
    path("<int:post_id>/", ListCreateComment.as_view(), name="list-create-post-comment"),
]

follow_patterns = [
    path('me/followers/', ListFollowers.as_view(), name='list-followers'),
    path('me/following/', ListFollowing.as_view(), name='list-following'),
    path('toggle-follow/<int:social_profile_id>/', FollowUnfollowUser.as_view(), name='follow-unfollow-user'),
]
friend_patterns = [
    path('profile/<int:social_profile_id>/', CreateFriendRequest.as_view(), name='create-friend-request'),
]

urlpatterns = [
    path('posts/', include(post_patterns)),
    path('comments/', include(comment_patterns)),
    path('followers/', include(follow_patterns)),
    path('friends/', include(friend_patterns)),
]
