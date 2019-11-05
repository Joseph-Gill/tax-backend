from django.urls import path, include
from app.social.views.comments import ListCreateComment
from app.social.views.followers import ListFollowers, ListFollowing, FollowUnfollowUser
from app.social.views.friends import CreateFriendRequest, RetrieveUpdateDestroyFriendRequest, ListFriends, \
    ListFriendRequests
from app.social.views.posts import ListCreatePosts, RetrieveUpdateDestroyPost, ListPostsUser, ListPostsLoggedInUser, \
    ListPostsFollowees, ListLikes, CreateLike, ListFriendsPosts
from app.social.views.profiles import ListSocialProfiles, RetrieveSocialProfiles, \
    RetrieveUpdateDestroyLoggedInUserSocialProfiles

post_patterns = [
    path('', ListCreatePosts.as_view(), name='list-create-posts'),
    path('<int:post_id>/', RetrieveUpdateDestroyPost.as_view(), name='retrieve-update-destroy-post'),
    path('profile/<int:social_profile_id>/', ListPostsUser.as_view(), name='list-posts-user'),
    path('me/', ListPostsLoggedInUser.as_view(), name='list-posts-logged-in-user'),
    path("following/", ListPostsFollowees.as_view(), name="list-posts-followees"),
    path("likes/", ListLikes.as_view(), name="list-liked-posts"),
    path("toggle-like/<int:post_id>/", CreateLike.as_view(), name="toggle-like"),
    path('friends/', ListFriendsPosts.as_view(), name='list-friend-posts'),

]

comment_patterns = [
    path("<int:post_id>/", ListCreateComment.as_view(), name="list-create-post-comment"),
]

follow_patterns = [
    path('followers/', ListFollowers.as_view(), name='list-followers'),
    path('following/', ListFollowing.as_view(), name='list-following'),
    path('toggle-follow/<int:social_profile_id>/', FollowUnfollowUser.as_view(), name='follow-unfollow-user'),
]
friend_patterns = [
    path('request/<int:social_profile_id>/', CreateFriendRequest.as_view(), name='create-friend-request'),
    path('requests/<int:friend_request_id>/', RetrieveUpdateDestroyFriendRequest.as_view(),
         name='retrieve-update-destroy-friend-request'),
    path('requests/', ListFriendRequests.as_view(), name='list-friend-request'),
    path('', ListFriends.as_view(), name='list-friends'),
]

profile_patterns = [
    path('', ListSocialProfiles.as_view(), name='list-social-profile'),
    path('<int:social_profile_id>/', RetrieveSocialProfiles.as_view(), name='retrieve-social-profile'),
    path('me/', RetrieveUpdateDestroyLoggedInUserSocialProfiles.as_view(),
         name='retrieve-update-destroy-logged-in-user-social-profile'),
]

urlpatterns = [
    path('posts/', include(post_patterns)),
    path('comments/', include(comment_patterns)),
    path('followers/', include(follow_patterns)),
    path('friends/', include(friend_patterns)),
    path('profile/', include(profile_patterns)),
]
