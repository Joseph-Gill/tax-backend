from django.urls import path

from app.userProfiles.views import RetrieveUpdateLoggedInUserProfile, RetrieveLoggedInUserTasks, CreateUpdateSpecificUserSpecificProjectRole

urlpatterns = [
    path('me/', RetrieveUpdateLoggedInUserProfile.as_view(), name='retrieve-update-userProfile'),
    path('tasks/me/', RetrieveLoggedInUserTasks.as_view(), name='retrieve-user-tasks'),
    path('project/<int:project_id>/role/<int:user_id>/', CreateUpdateSpecificUserSpecificProjectRole.as_view(), name='update-user-group-or-project-role')
]