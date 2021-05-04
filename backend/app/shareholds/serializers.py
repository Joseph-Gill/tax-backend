from rest_framework import serializers
from app.shareholds.models import Sharehold


class ShareholdSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sharehold
        fields = ['id', 'parent', 'child', 'percent_ownership']
