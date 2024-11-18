from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import Mission
from cats.models import Cats

class MissionsAPITest(TestCase):
    def setUp(self):
        """
        Set up test data and API client for the test cases.
        """
        self.client = APIClient()
        self.cat = Cats.objects.create(
            name="Agent Paws", years_of_experience=3, breed="Maine Coon", salary="7000.00"
        )
        self.valid_data = {
            "cat": self.cat.id,
            "status": False,
            "targets": [
                {"title": "Target Alpha", "country": "USA", "notes": "Observation 1"},
                {"title": "Target Beta", "country": "UK", "notes": "Observation 2"}
            ]
        }


    def test_delete_mission_with_assigned_cat(self):
        """
        Test attempting to delete a mission that has an assigned cat.
        """
        mission = Mission.objects.create(cat=self.cat)
        response = self.client.delete(f'/api/missions/{mission.id}/')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Mission.objects.count(), 1)

    def test_get_missions_list(self):
        """
        Test retrieving a list of missions.
        """
        Mission.objects.create(cat=self.cat)
        response = self.client.get('/api/missions/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_list_missions(self):
        """
        Test listing missions.
        """
        Mission.objects.create(cat=self.cat, status=False)
        response = self.client.get('/api/missions/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_get_single_mission(self):
        """
        Test retrieving a single mission.
        """
        mission = Mission.objects.create(cat=self.cat, status=False)
        response = self.client.get(f'/api/missions/{mission.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['cat'], self.cat.id)
