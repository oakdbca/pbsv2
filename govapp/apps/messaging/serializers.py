from rest_framework import serializers

from govapp.apps.accounts.serializers import UserSerializer
from govapp.apps.main.serializers import KeyObjectSerializerMixin
from govapp.apps.messaging.models import Message, MessageBatch


class MessageBatchSerializer(serializers.ModelSerializer):
    type_display = serializers.CharField(source="get_type_display")

    class Meta:
        model = MessageBatch
        fields = "__all__"


class MessageSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    sender = UserSerializer()
    type_display = serializers.CharField(source="get_type_display")

    class Meta:
        model = Message
        fields = "__all__"


class MessageKeyObjectSerializer(KeyObjectSerializerMixin, MessageSerializer):
    pass
