import logging

from django.contrib.contenttypes.models import ContentType
from rest_framework import serializers

from govapp.apps.main.models import District, Region

logger = logging.getLogger(__name__)


class ContentTypeSerializerMixin:
    def to_representation(self, instance):
        logger.debug(f"to_representation: {type(instance)}")
        ret = super().to_representation(instance)
        # TODO: This will cause N+1 queries, need to optimize
        # in cases where union of multiple models is used this will be necesary
        # however in all other cases it is not
        content_type = ContentType.objects.get_for_model(instance)
        ret["content_type"] = content_type.id
        ret["content_type_model"] = content_type.model
        ret["verbose_name"] = instance._meta.verbose_name
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
