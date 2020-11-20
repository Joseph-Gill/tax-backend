from django.urls import path

from app.groups.views import ListAllOrCreateGroup, RetrieveUpdateDestroySpecificGroup

urlpatterns = [
    path('', ListAllOrCreateGroup.as_view(), name='list-create-group'),
    path('/group/<int:group_id>/', RetrieveUpdateDestroySpecificGroup.as_view(), name='retrieve-update-destroy-group')
]