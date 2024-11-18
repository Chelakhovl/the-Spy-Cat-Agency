from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import Cats


class SpyCatsAPITest(TestCase):
    """
    Test suite for the SpyCats API endpoints.
    """

    def setUp(self):
        """
        Set up the test client and sample data.
        """
        self.client = APIClient()
        self.valid_data = {
            "name": "Agent Whiskers",
            "years_of_experience": 5,
            "breed": "Siberian",
            "salary": "5000.00"
        }

    def test_create_spycat(self):
        """
        Test the creation of a new spy cat.
        Validates that a cat is successfully created and saved in the database.
        """
        response = self.client.post('/api/cats/', self.valid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Cats.objects.count(), 1)
        self.assertEqual(Cats.objects.get().name, "Agent Whiskers")

    def test_update_salary(self):
        """
        Test updating the salary of an existing spy cat.
        Validates that the salary is updated correctly.
        """
        spy_cat = Cats.objects.create(**self.valid_data)
        response = self.client.patch(f'/api/cats/{spy_cat.id}/', {"salary": "6000.00"}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Cats.objects.get().salary, 6000.00)

    def test_get_spy_cats_list(self):
        """
        Test retrieving a list of all spy cats.
        Validates that the correct data is returned in the response.
        """
        Cats.objects.create(**self.valid_data)
        response = self.client.get('/api/cats/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_get_single_spy_cat(self):
        """
        Test retrieving the details of a single spy cat by its ID.
        Validates that the correct data is returned for the specified cat.
        """
        spy_cat = Cats.objects.create(**self.valid_data)
        response = self.client.get(f'/api/cats/{spy_cat.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], "Agent Whiskers")

    def test_delete_spy_cat(self):
        """
        Test deleting an existing spy cat by its ID.
        Validates that the cat is removed from the database.
        """
        spy_cat = Cats.objects.create(**self.valid_data)
        response = self.client.delete(f'/api/cats/{spy_cat.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Cats.objects.count(), 0)
