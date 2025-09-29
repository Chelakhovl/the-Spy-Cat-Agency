from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from missions.models import Mission, Target
from cats.models import Cat


class TargetAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.cat = Cat.objects.create(
            name="Agent Pawson",
            years_of_experience=2,
            breed="Siberian",
            salary="6000.00",
        )
        self.mission = Mission.objects.create(cat=self.cat)
        self.target_data = {
            "mission": self.mission.id,
            "title": "Target One",
            "country": "France",
            "notes": "High priority",
            "is_completed": False,
        }

    def test_create_mission_with_targets(self):
        """Тепер створюємо таргети тільки через місію"""
        data = {
            "cat": self.cat.id,
            "is_completed": False,
            "targets": [
                {"title": "Target A", "country": "USA", "notes": "Secret"},
                {"title": "Target B", "country": "UK", "notes": "Observation"},
            ],
        }
        response = self.client.post("/api/missions/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        mission = Mission.objects.first()
        self.assertEqual(mission.targets.count(), 2)
        self.assertEqual(mission.targets.first().title, "Target A")

    def test_list_targets(self):
        Target.objects.create(mission=self.mission, title="T1", country="FR")
        response = self.client.get("/api/targets/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_get_single_target(self):
        target = Target.objects.create(mission=self.mission, title="T1", country="FR")
        response = self.client.get(f"/api/targets/{target.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "T1")

    def test_update_target(self):
        target = Target.objects.create(mission=self.mission, title="Old", country="FR")
        response = self.client.patch(
            f"/api/targets/{target.id}/", {"title": "New"}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        target.refresh_from_db()
        self.assertEqual(target.title, "New")

    def test_delete_target(self):
        target = Target.objects.create(mission=self.mission, title="T1", country="FR")
        response = self.client.delete(f"/api/targets/{target.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Target.objects.count(), 0)
