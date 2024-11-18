from rest_framework import viewsets
from .models import Cats
from .serializers import SpyCatSerializer

class SpyCatViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing spy cats.
    Supports CRUD operations (Create, Read, Update, Delete).
    """
    queryset = Cats.objects.all()
    serializer_class = SpyCatSerializer
