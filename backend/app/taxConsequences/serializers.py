from rest_framework import serializers
from app.taxConsequences.models import TaxConsequence


class TaxConsequenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaxConsequence
        fields = ['id', 'location', 'type', 'description', 'created', 'updated']
