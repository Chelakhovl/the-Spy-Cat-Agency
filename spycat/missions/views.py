from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Mission, Target
from .serializers import MissionSerializer, TargetSerializer


class MissionViewSet(viewsets.ModelViewSet):
    """
    A viewset for handling CRUD operations for missions.
    Includes custom actions for completing targets and restricting deletion of missions with assigned spy cats.
    """
    queryset = Mission.objects.all()
    serializer_class = MissionSerializer

    @action(detail=True, methods=['patch'])
    def complete_target(self, request, pk=None):
        """
        Marks a specific target as completed.
        """
        target_id = request.data.get('target_id')
        if not target_id:
            return Response({"error": "Target ID is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            target = Target.objects.get(pk=target_id, mission_id=pk)
            target.is_completed = True
            target.save()
            return Response({"message": f"Target '{target.title}' marked as completed."})
        except Target.DoesNotExist:
            return Response({"error": "Target not found."}, status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, *args, **kwargs):
        """
        Prevents deletion of a mission if a spy cat is assigned.
        """
        mission = self.get_object()
        if mission.spy_cat:
            return Response(
                {"error": "Cannot delete a mission assigned to a spy cat."},
                status=status.HTTP_400_BAD_REQUEST
            )
        return super().destroy(request, *args, **kwargs)


class TargetViewSet(viewsets.ModelViewSet):
    """
    A viewset for handling CRUD operations for targets.
    """
    queryset = Target.objects.all()
    serializer_class = TargetSerializer
