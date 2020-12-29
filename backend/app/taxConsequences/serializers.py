from rest_framework import serializers
from app.taxConsequences.models import TaxConsequence
from app.userProfiles.models import UserProfile
from app.users.serializers import UserSerializer


class TaxConsequenceUserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(
        required=False
    )

    class Meta:
        model = UserProfile
        fields = ['user']


class TaxConsequenceSerializer(serializers.ModelSerializer):
    creating_user = TaxConsequenceUserProfileSerializer(
        required=False
    )

    reviewing_user = TaxConsequenceUserProfileSerializer(
        required=False
    )

    class Meta:
        model = TaxConsequence
        fields = ['id', 'location', 'type', 'description', 'reviewed', 'created', 'updated', 'reviewing_user', 'creating_user']
