from rest_framework import serializers

from app.taskDocuments.models import TaskDocument


class TaskDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskDocument
        fields = ['id', 'created', 'updated', 'document']
