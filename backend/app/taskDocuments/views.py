from rest_framework.generics import DestroyAPIView
from app.taskDocuments.models import TaskDocument


class DestroySpecifiedTaskDocument(DestroyAPIView):
    """
    Destroy specified Task Document
    """
    queryset = TaskDocument.objects.all()
    lookup_url_kwarg = 'taskdocument_id'
