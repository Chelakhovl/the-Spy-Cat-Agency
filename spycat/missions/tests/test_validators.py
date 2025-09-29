from django.test import TestCase
from rest_framework.exceptions import ValidationError
from missions.serializers import MissionSerializer
from cats.serializers import SpyCatSerializer
from cats.models import Cat


class ValidatorsTest(TestCase):
    def setUp(self):
        self.cat = Cat.objects.create(
            name="Agent Paws", years_of_experience=3, breed="Siberian", salary="5000"
        )

    def test_cat_breed_validator_fails(self):
        serializer = SpyCatSerializer(
            data={
                "name": "Agent X",
                "years_of_experience": 1,
                "breed": "Nonexistent Breed",
                "salary": "4000",
            }
        )
        serializer.is_valid()
        self.assertIn("breed", serializer.errors)

    def test_mission_targets_validator_fails(self):
        mission_data = {"cat": self.cat.id, "is_completed": False, "targets": []}
        serializer = MissionSerializer(data=mission_data)
        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)

    def test_mission_targets_validator_success(self):
        mission_data = {
            "cat": self.cat.id,
            "is_completed": False,
            "targets": [
                {"title": "T1", "country": "US"},
                {"title": "T2", "country": "UK"},
            ],
        }
        serializer = MissionSerializer(data=mission_data)
        self.assertTrue(serializer.is_valid())
