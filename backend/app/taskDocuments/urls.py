from django.urls import path
from app.taskDocuments.views import DestroySpecifiedTaskDocument

urlpatterns = [
    path('<int:taskdocument_id>/', DestroySpecifiedTaskDocument.as_view(), name='destroy-task-document')
]