from django.urls import path

from app.userProfiles.views import RetrieveUpdateLoggedInUserProfile, RetrieveLoggedInUserTasks, UpdateSpecificUserGroupOrProjectRole

urlpatterns = [
    path('me/', RetrieveUpdateLoggedInUserProfile.as_view()),
    path('tasks/me/', RetrieveLoggedInUserTasks.as_view()),
    path('permissions/<int:user_id>', UpdateSpecificUserGroupOrProjectRole.as_view())
]