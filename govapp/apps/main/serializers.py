from typing import ClassVar, Generic, TypeVar

from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
from rest_framework import serializers

from govapp.helpers import get_model_by_reference_number

from .models import District, Region

T = TypeVar("T")
MT = TypeVar("MT")  # Model type


class GenericKeyValueSerializer(serializers.Serializer, Generic[T, MT]):
    """A serializer for key-value pairs of a model.
    By default, the key is the model's id and the value is the model's display_name or name field.
    This can be overridden by setting the key and value fields on the subclass.

    Example usage:
        ```
        class MyKeyValueModelSerializer(
            serializers.ModelSerializer,
            GenericKeyValueSerializer[serializers.ModelSerializer, MyModel],
        ):
            key = ...  # Override the key field
            value = ... # Override the value field

            class Meta(GenericKeyValueSerializer.Meta):
                model = MyModel
        ```
    """

    key: ClassVar[serializers.Field] = serializers.IntegerField(source="id")
    value: ClassVar[serializers.Field] = serializers.SerializerMethodField()

    class Meta:
        model = MT
        fields = ["key", "value"]
        read_only_fields = ["key", "value"]

    def get_value(self, obj):
        display_name = getattr(obj, "display_name", None)
        if not display_name:
            return getattr(obj, "name", "No display_name or name field found on model")
        return display_name


class ContentTypeSerializerMixin:
    def to_representation(self, instance):
        ret = super().to_representation(instance)
        # TODO: This will cause N+1 queries, need to optimize
        # in cases where union of multiple models is used this will be necesary
        # however in all other cases it is not
        content_type = ContentType.objects.get_for_model(instance)
        ret["content_type"] = content_type.id
        ret["content_type_model"] = content_type.model
        ret["verbose_name"] = instance._meta.verbose_name
        return ret


class KeyObjectSerializerMixin:
    def to_representation(self, instance):
        row = super().to_representation(instance)
        return {row["id"]: row}


class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = "__all__"


class DistrictSerializer(serializers.ModelSerializer):
    region = RegionSerializer()

    class Meta:
        model = District
        fields = "id", "name", "region"


class SearchSerializer(serializers.Serializer):
    reference_number = serializers.CharField(allow_null=True, required=False)
    name = serializers.CharField(allow_null=True, required=False)
    status = serializers.CharField(allow_null=True, required=False)
    status_display = serializers.CharField(
        source="get_status_display", allow_null=True, required=False
    )

    class Meta:
        fields = [
            "id",
            "reference_number",
            "name",
            "status",
            "status_display",
        ]

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        model = get_model_by_reference_number(instance.reference_number)
        verbose_name = model._meta.verbose_name
        ret["verbose_name"] = verbose_name
        viewname = verbose_name.replace(" ", "-").lower() + "-detail"
        ret["link"] = self.context.get("request").build_absolute_uri(
            reverse(viewname, args=[instance.id])
        )
        return ret
