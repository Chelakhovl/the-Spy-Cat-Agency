import requests
from django.conf import settings


def validate_breed_from_api(breed_name: str) -> bool:
    """
    Validate cat breed using TheCatAPI.
    Returns True if breed exists, False otherwise.
    """
    try:
        response = requests.get(settings.THE_CAT_API_URL, timeout=5)
        response.raise_for_status()
        breeds = response.json()
        breed_names = [breed.get("name") for breed in breeds if "name" in breed]
        return breed_name in breed_names
    except (requests.RequestException, ValueError, TypeError):
        return False
