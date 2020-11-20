from django.urls import path

from app.userProfiles.views import RetrieveUpdateLoggedInUserProfile, RetrieveLoggedInUserTasks, UpdateSpecificUserGroupOrProjectRole

urlpatterns = [
    path('me/', RetrieveUpdateLoggedInUserProfile.as_view(), name='retrieve-update-userProfile'),
    path('tasks/me/', RetrieveLoggedInUserTasks.as_view(), name='retrieve-user-tasks'),
    path('permissions/<int:user_id>', UpdateSpecificUserGroupOrProjectRole.as_view(), name='update-user-group-or-project-role')
]