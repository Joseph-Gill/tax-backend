from django.urls import path
from app.projectRoles.views import ListRolesForSpecifiedUserProfileGroup

urlpatterns = [
    path('userprofile/<int:userprofile_id>/group/<int:group_id>/', ListRolesForSpecifiedUserProfileGroup.as_view(), name='retrieve-roles-user-group')
]
