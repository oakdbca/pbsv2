from django.db.models.query import QuerySet
from django_filters import rest_framework as filters
from rest_framework import viewsets
from rest_framework_datatables.django_filters.backends import DatatablesFilterBackend

from govapp.apps.main.mixins import KeyValueListMixin

from .models import District, Region
from .serializers import DistrictSerializer, RegionSerializer


class DjangoFiltersModelViewSet(viewsets.ModelViewSet):
    """Base class for viewsets that use DjangoFilters
    Uses django-filter's filterset_class attribute if the action is in the list of actions.
    Otherwise uses the default filter_queryset method.
    """

    filter_backends = [DatatablesFilterBackend, filters.DjangoFilterBackend]
    actions = ["list"]  # The actions that will use the django_filters filterset_class

    @property
    def filterset_class(self):
        if self.action in self.actions:
            if not hasattr(self, "django_filters_filterset_class"):
                raise AttributeError(
                    f"Expected {self.__class__.__name__} to have a django_filters_filterset_class attribute"
                )
            return self.django_filters_filterset_class
        return None

    def filter_queryset(self, queryset: QuerySet) -> QuerySet:
        # If the action is in the list of actions then use the filterset_class
        if self.filterset_class:
            return self.filterset_class(self.request.GET, queryset=self.queryset).qs
        return super().filter_queryset(queryset)


class RegionViewSet(KeyValueListMixin, viewsets.GenericViewSet):
    """Region viewset"""

    queryset = Region.objects.all()
    serializer_class = RegionSerializer


class DistrictViewSet(KeyValueListMixin, viewsets.GenericViewSet):
    """District viewset"""

    queryset = District.objects.all()
    serializer_class = DistrictSerializer
