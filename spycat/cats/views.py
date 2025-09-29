from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Cat
from .serializers import SpyCatSerializer
from .services import update_cat_salary


class SpyCatViewSet(viewsets.ModelViewSet):
    queryset = Cat.objects.all()
    serializer_class = SpyCatSerializer

    @action(detail=True, methods=["patch"], url_path="update-salary")
    def update_salary(self, request, pk=None):
        cat = self.get_object()
        salary = request.data.get("salary")
        if salary is None:
            return Response(
                {"error": "Salary is required"}, status=status.HTTP_400_BAD_REQUEST
            )

        updated_cat = update_cat_salary(cat, salary)
        return Response(
            {"message": "Salary updated successfully", "salary": updated_cat.salary}
        )
