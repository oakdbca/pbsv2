from rest_framework import response
from rest_framework.decorators import action

from govapp.apps.main.serializers import GenericKeyValueSerializer


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
                else "name" if "name" in field_names else None
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

        class NamedModelKeyValueSerializer(
            serializers.ModelSerializer,
            GenericKeyValueSerializer[serializers.ModelSerializer, class_model],
        ):
            key = serializers.IntegerField(source="id")

            class Meta(GenericKeyValueSerializer.Meta):
                model = class_model

        return NamedModelKeyValueSerializer


class ChoicesKeyValueListMixin:
    """A mixin for viewsets that return a list of key-value pairs for the available choices of a model field."""

    @action(detail=False, methods=["get"], url_path="key-value-list")
    def key_value_list(self, request):
        if not hasattr(self, "choices_dict"):
            raise AttributeError("choices_dict is not defined on viewset")

        return response.Response(
            [{"key": s[0], "value": s[1]} for s in self.choices_dict.items()]
        )
