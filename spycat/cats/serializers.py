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
        response = requests.get(f"{settings.THE_CAT_API_URL}")
        if response.status_code != 200:
            raise serializers.ValidationError("Unable to validate breed at this time.")

        breeds = response.json()
        breed_names = [breed['name'] for breed in breeds]

        if value not in breed_names:
            raise serializers.ValidationError("Invalid breed. Please provide a valid cat breed.")

        return value
