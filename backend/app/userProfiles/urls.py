from django.urls import path
from app.userProfiles.views import RetrieveUpdateLoggedInUserProfile, RetrieveLoggedInUserTasks, CreateUpdateSpecificUserSpecificProjectRole, RetrieveSpecificUser

urlpatterns = [
    path('me/', RetrieveUpdateLoggedInUserProfile.as_view(), name='retrieve-update-userProfile'),
    path('tasks/me/', RetrieveLoggedInUserTasks.as_view(), name='retrieve-user-tasks'),
    path('group/<int:group_id>/userprofile/<int:userprofile_id>/', CreateUpdateSpecificUserSpecificProjectRole.as_view(), name='update-user-group-or-project-role'),
    path('userprofile/<int:userprofile_id>/', RetrieveSpecificUser.as_view(), name='retrieve-specific-user')
]