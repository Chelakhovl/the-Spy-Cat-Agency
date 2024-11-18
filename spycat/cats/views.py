from rest_framework import viewsets
from .models import Cats
from .serializers import SpyCatSerializer
import requests
from rest_framework.response import Response
from rest_framework import status

class SpyCatViewSet(viewsets.ModelViewSet):
    queryset = Cats.objects.all()
    serializer_class = SpyCatSerializer

    def create(self, request, *args, **kwargs):
        breed = request.data.get('breed')
        response = requests.get(f'https://api.thecatapi.com/v1/breeds/search?q={breed}')
        if not response.json():
            return Response({"error": "Invalid breed"}, status=status.HTTP_400_BAD_REQUEST)
        return super().create(request, *args, **kwargs)
