from django.urls import path

from app.users.views import ListUsers, RetrieveUser, RetrieveUpdateDestroyLoggedInUser, RetrieveAllUsersForSpecificGroup

urlpatterns = [
    path('', ListUsers.as_view(), name='list-users'),
    path('<int:user_id>/', RetrieveUser.as_view(), name='retrieve-user'),
    path('me/', RetrieveUpdateDestroyLoggedInUser.as_view(), name='retrieve-update-destroy-logged-in-user'),
    path('groups/<int:group_id>/', RetrieveAllUsersForSpecificGroup.as_view(), name='retrieve-users-for-group')
]
