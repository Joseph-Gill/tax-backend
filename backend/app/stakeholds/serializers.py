from rest_framework import serializers
from app.stakeholds.models import Stakehold


class StakeholdSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stakehold
        fields = ['id', 'parent', 'child', 'percent_ownership']
