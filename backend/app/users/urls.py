from django.urls import path

from app.users.views import ListUsers, RetrieveUser, RetrieveUpdateDestroyLoggedInUser, ListFollowers, ListFollowing, \
    FollowUnfollowUser

urlpatterns = [
    path('', ListUsers.as_view(), name='list-users'),
    path('<int:pk>/', RetrieveUser.as_view(), name='retrieve-user'),
    path('me/', RetrieveUpdateDestroyLoggedInUser.as_view(), name='retrieve-update-destroy-logged-in-user'),
    path('me/followers/', ListFollowers.as_view(), name='list-followers'),
    path('me/following/', ListFollowing.as_view(), name='list-following'),
    path('toggle-follow/<int:pk>/', FollowUnfollowUser.as_view(), name='follow-unfollow-user'),
]
