from rest_framework import serializers
from .models import Cats
from django.conf import settings
import requests

class SpyCatSerializer(serializers.ModelSerializer):
    """
    Serializer for the Cats model.
    Validates the breed of the spy cat using TheCatAPI.
    """
    class Meta:
        model = Cats
        fields = '__all__'

    def validate_breed(self, value):
        """
        Validates that the provided breed exists in TheCatAPI.
        """
        response = requests.get(f"{settings.THE_CAT_API_URL}?q={value}")
        if not response.json():
            raise serializers.ValidationError("Invalid breed. Please provide a valid cat breed.")
        return value
