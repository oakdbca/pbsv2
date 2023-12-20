# from django.shortcuts import render
from django.db.models.query import QuerySet
from rest_framework import viewsets

from .models import BurnPlanElement
from .serializers import BurnPlanElementSerializer


class BurnPlanElementViewSet(viewsets.ModelViewSet):
    queryset = BurnPlanElement.objects.none()
    serializer_class = BurnPlanElementSerializer
    # permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self) -> QuerySet:
        pk = self.kwargs.get("pk", None)
        if pk:
            return BurnPlanElement.objects.filter(pk=pk)
        return super().get_queryset()
