from django.db import models
from cats.models import Cat


class Mission(models.Model):
    """
    Represents a spy mission assigned to a specific cat.
    Each mission can have multiple targets and a single assigned cat.
    """

    cat = models.ForeignKey(
        Cat,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="missions",
        help_text="The cat assigned to this mission. Can be null.",
    )
    is_completed = models.BooleanField(
        default=False, help_text="The completion status of the mission."
    )
    created_at = models.DateTimeField(
        auto_now_add=True, help_text="The date and time when the mission was created."
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Mission {self.id} (Completed: {self.is_completed})"


class Target(models.Model):
    """
    Represents a target associated with a specific mission.
    """

    mission = models.ForeignKey(
        Mission,
        on_delete=models.CASCADE,
        related_name="targets",
        help_text="The mission this target is associated with.",
    )
    title = models.CharField(
        max_length=200, help_text="The title or name of the target."
    )
    country = models.CharField(
        max_length=100, help_text="The country where the target is located."
    )
    notes = models.TextField(
        blank=True,
        null=True,
        help_text="Additional notes or observations about the target.",
    )
    is_completed = models.BooleanField(
        default=False, help_text="The completion status of the target."
    )

    class Meta:
        ordering = ["title"]

    def __str__(self):
        return f"{self.title} ({'Done' if self.is_completed else 'In progress'})"
