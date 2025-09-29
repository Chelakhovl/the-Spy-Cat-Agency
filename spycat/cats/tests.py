from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from unittest.mock import patch
from cats.models import Cat


class SpyCatsAPITest(TestCase):
    """
    Unit tests for SpyCats API endpoints.
    Covers CRUD operations with mocked TheCatAPI validation.
    """

    def setUp(self):
        self.client = APIClient()
        self.valid_data = {
            "name": "Agent Whiskers",
            "years_of_experience": 5,
            "breed": "Siberian",
            "salary": "5000.00",
        }

        # Patch TheCatAPI validation for all tests
        patcher = patch("cats.utils.validate_breed_from_api", return_value=True)
        self.mock_validate = patcher.start()
        self.addCleanup(patcher.stop)

    def test_create_spycat(self):
        """Test creating a new spy cat via API."""
        response = self.client.post("/api/cats/", self.valid_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Cat.objects.count(), 1)
        self.assertEqual(Cat.objects.get().name, "Agent Whiskers")

    def test_update_salary(self):
        """Test updating salary of an existing spy cat."""
        spy_cat = Cat.objects.create(**self.valid_data)
        response = self.client.patch(
            f"/api/cats/{spy_cat.id}/", {"salary": "6000.00"}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        spy_cat.refresh_from_db()
        self.assertEqual(float(spy_cat.salary), 6000.00)

    def test_get_spy_cats_list(self):
        """Test retrieving the list of all spy cats."""
        Cat.objects.create(**self.valid_data)
        response = self.client.get("/api/cats/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_get_single_spy_cat(self):
        """Test retrieving details of a single spy cat by ID."""
        spy_cat = Cat.objects.create(**self.valid_data)
        response = self.client.get(f"/api/cats/{spy_cat.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Agent Whiskers")

    def test_delete_spy_cat(self):
        """Test deleting an existing spy cat by ID."""
        spy_cat = Cat.objects.create(**self.valid_data)
        response = self.client.delete(f"/api/cats/{spy_cat.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Cat.objects.count(), 0)
