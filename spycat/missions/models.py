from django.db import models
from cats.models import Cats


class Mission(models.Model):
    """
    Represents a spy mission assigned to a specific cat.
    Each mission can have multiple targets and a single assigned cat.
    Attributes:
        cat (Cats): The cat assigned to the mission (optional, can be null).
        status (bool): Indicates whether the mission is completed.
        created_at (datetime): The timestamp when the mission was created.
    """
    cat = models.OneToOneField(
        Cats, on_delete=models.SET_NULL, null=True, blank=True,
        help_text="The cat assigned to this mission. Can be null."
    )
    status = models.BooleanField(
        default=False, 
        help_text="The completion status of the mission."
    )
    created_at = models.DateTimeField(
        auto_now_add=True, 
        help_text="The date and time when the mission was created."
    )

    def __str__(self):
        return f"Mission {self.id}"


class Target(models.Model):
    """
    Represents a target associated with a specific mission.
    A target includes details like title, country, notes, and completion status.
    Attributes:
        mission (Mission): The mission to which the target belongs.
        title (str): The title or name of the target.
        country (str): The country where the target is located.
        notes (str): Additional notes or observations about the target.
        is_completed (bool): Indicates whether the target is completed.
    """
    mission = models.ForeignKey(
        Mission, on_delete=models.CASCADE, related_name='targets',
        help_text="The mission this target is associated with."
    )
    title = models.CharField(
        max_length=200, 
        help_text="The title or name of the target."
    )
    country = models.CharField(
        max_length=100, 
        help_text="The country where the target is located."
    )
    notes = models.TextField(
        blank=True, null=True, 
        help_text="Additional notes or observations about the target."
    )
    is_completed = models.BooleanField(
        default=False, 
        help_text="The completion status of the target."
    )

    def save(self, *args, **kwargs):
        if self.pk and self.is_completed and 'is_completed' not in kwargs.get('update_fields', []):
            raise ValueError("Cannot update a completed target.")
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
