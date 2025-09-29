from django.shortcuts import get_object_or_404
from .models import Mission, Target


def complete_target(mission_id: int, target_id: int) -> Target:
    """
    Marks a target as completed for a given mission.
    Raises 404 if target does not exist.
    """
    target = get_object_or_404(Target, pk=target_id, mission_id=mission_id)
    target.is_completed = True
    target.save()
    return target


def delete_mission_if_no_cat(mission: Mission) -> bool:
    """
    Returns True if mission can be deleted, False if a spy cat is assigned.
    """
    if mission.cat:
        return False
    mission.delete()
    return True


def mark_mission_completed_if_all_targets_done(mission: Mission) -> bool:
    """
    Marks mission as completed if all targets are done.
    Returns True if completed, False otherwise.
    """
    if not mission.targets.filter(is_completed=False).exists():
        mission.is_completed = True
        mission.save()
        return True
    return False
