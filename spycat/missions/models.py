from django.db import models
from cats.models import Cats

class Mission(models.Model):
    cat = models.OneToOneField(
        Cats, on_delete=models.SET_NULL, null=True, blank=True
    )
    status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Mission {self.id}"


class Target(models.Model):
    mission = models.ForeignKey(Mission, on_delete=models.CASCADE, related_name='targets')
    title = models.CharField(max_length=200)
    country = models.CharField(max_length=100)
    notes = models.TextField(blank=True, null=True)
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return self.title

