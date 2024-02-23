from typing import ClassVar, Generic, TypeVar

from rest_framework import serializers

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


class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = "__all__"


class DistrictSerializer(serializers.ModelSerializer):
    region = RegionSerializer()

    class Meta:
        model = District
        fields = "__all__"
