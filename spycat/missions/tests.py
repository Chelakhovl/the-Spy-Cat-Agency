from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import Mission, Target
from cats.models import Cats


class MissionsAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.cat = Cats.objects.create(name="Agent Paws", years_of_experience=3, breed="Maine Coon", salary="7000.00")
        self.valid_data = {
            "cat": self.cat.id,
            "status": False,
            "targets": [
                {"title": "Target Alpha", "country": "USA", "notes": "Observation 1"},
                {"title": "Target Beta", "country": "UK", "notes": "Observation 2"}
            ]
        }

    def test_create_mission_with_targets(self):
        response = self.client.post('/api/missions/', self.valid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Mission.objects.count(), 1)
        self.assertEqual(Target.objects.count(), 2)

    def test_complete_target(self):
        mission = Mission.objects.create(cat=self.cat)
        target = Target.objects.create(mission=mission, title="Target Alpha", country="USA", notes="Test", is_completed=False)
        response = self.client.patch(
            f'/api/missions/{mission.id}/complete_target/',
            {"target_id": target.id},
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        target.refresh_from_db()
        self.assertTrue(target.is_completed)

    def test_delete_mission_with_assigned_cat(self):
        mission = Mission.objects.create(cat=self.cat)
        response = self.client.delete(f'/api/missions/{mission.id}/')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Mission.objects.count(), 1)

    def test_update_mission_targets(self):
        mission = Mission.objects.create(cat=self.cat)
        target = Target.objects.create(mission=mission, title="Target Alpha", country="USA", notes="Test")
        response = self.client.patch(
            f'/api/missions/{mission.id}/',
            {
                "targets": [
                    {"id": target.id, "title": "Updated Target Alpha", "country": "Canada", "notes": "Updated notes"}
                ]
            },
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        target.refresh_from_db()
        self.assertEqual(target.title, "Updated Target Alpha")
        self.assertEqual(target.country, "Canada")
        self.assertEqual(target.notes, "Updated notes")

    def test_get_missions_list(self):
        Mission.objects.create(cat=self.cat)
        response = self.client.get('/api/missions/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)