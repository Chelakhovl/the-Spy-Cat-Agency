from rest_framework import serializers
from .models import Cat
from .utils import validate_breed_from_api


class SpyCatSerializer(serializers.ModelSerializer):
    """
    Serializer for the Cat model.
    Validates the breed of the spy cat using TheCatAPI.
    """

    class Meta:
        model = Cat
        fields = "__all__"

    def validate_breed(self, value):
        """
        Validate the cat breed using TheCatAPI via utils function.
        """
        if not validate_breed_from_api(value):
            raise serializers.ValidationError(
                f"Invalid breed '{value}'. Please provide a valid cat breed."
            )
        return value
