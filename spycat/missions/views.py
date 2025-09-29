from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Mission, Target
from .serializers import MissionSerializer, TargetSerializer
from .services import (
    complete_target,
    delete_mission_if_no_cat,
    mark_mission_completed_if_all_targets_done,
)


class MissionViewSet(viewsets.ModelViewSet):
    queryset = Mission.objects.all()
    serializer_class = MissionSerializer

    @action(detail=True, methods=["patch"])
    def complete_target(self, request, pk=None):
        """
        Marks a specific target as completed.
        """
        target_id = request.data.get("target_id")
        if not target_id:
            return Response(
                {"error": "Target ID is required."}, status=status.HTTP_400_BAD_REQUEST
            )

        try:
            target = complete_target(pk, target_id)
            mark_mission_completed_if_all_targets_done(target.mission)
            return Response(
                {"message": f"Target '{target.title}' marked as completed."}
            )
        except Exception:
            return Response(
                {"error": "Target not found."}, status=status.HTTP_404_NOT_FOUND
            )

    def destroy(self, request, *args, **kwargs):
        """
        Prevents deletion of a mission if a spy cat is assigned.
        """
        mission = self.get_object()
        if not delete_mission_if_no_cat(mission):
            return Response(
                {"error": "Cannot delete a mission assigned to a spy cat."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response(status=status.HTTP_204_NO_CONTENT)


class TargetViewSet(viewsets.ModelViewSet):
    queryset = Target.objects.all()
    serializer_class = TargetSerializer

    def create(self, request, *args, **kwargs):
        return Response(
            {"error": "Targets can only be created through a mission."},
            status=status.HTTP_405_METHOD_NOT_ALLOWED,
        )
