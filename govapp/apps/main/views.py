from rest_framework import response, viewsets
from rest_framework.decorators import action

from .models import District, Region
from .serializers import DistrictSerializer, RegionSerializer


class KeyValueListMixin:
    @action(detail=False, methods=["get"], url_path="key-value-list")
    def key_value_list(self, request):
        if hasattr(self, "key_value_display_field"):
            key_value_display_field = self.key_value_display_field
        else:
            class_model = self.get_serializer().Meta.model
            field_names = [field.name for field in class_model._meta.get_fields()]
            key_value_display_field = (
                "display_name"
                if "display_name" in field_names
                else "name"
                if "name" in field_names
                else None
            )
            if not key_value_display_field:
                raise AttributeError(
                    "key_value_display_field is not defined on viewset or model"
                )

        queryset = self.get_queryset().only("id", key_value_display_field)
        search_term = request.GET.get("term", "")
        if search_term:
            queryset = queryset.filter(
                **{f"{key_value_display_field}__icontains": search_term}
            )[:30]
        serializer_class = self.get_key_value_serializer_class()
        serializer = serializer_class(queryset, many=True)
        return response.Response(serializer.data)

    def get_key_value_serializer_class(self):
        if hasattr(self, "key_value_serializer_class"):
            return self.key_value_serializer_class

        class_model = self.get_serializer().Meta.model
        from rest_framework import serializers

        class NamedModelKeyValueSerializer(serializers.ModelSerializer):
            key = serializers.IntegerField(source="id")
            value = serializers.SerializerMethodField()

            class Meta:
                model = class_model
                fields = ["key", "value"]

            def get_value(self, obj):
                display_name = getattr(obj, "display_name", None)
                if not display_name:
                    return getattr(
                        obj, "name", "No display_name or name field found on model"
                    )
                return display_name

        return NamedModelKeyValueSerializer


class RegionViewSet(KeyValueListMixin, viewsets.GenericViewSet):
    """Region viewset"""

    queryset = Region.objects.all()
    serializer_class = RegionSerializer


class DistrictViewSet(KeyValueListMixin, viewsets.GenericViewSet):
    """District viewset"""

    queryset = District.objects.all()
    serializer_class = DistrictSerializer
