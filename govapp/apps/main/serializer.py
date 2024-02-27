# Third-Party
from django.contrib.contenttypes.models import ContentType
from rest_framework import serializers

from govapp.apps.main.models import District, Region


class ContentTypeModelSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret["content_type"] = ContentType.objects.get_for_model(instance).id
        return ret


class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = "__all__"


class DistrictSerializer(serializers.ModelSerializer):
    region = RegionSerializer()

    class Meta:
        model = District
        fields = "id", "name", "region"
