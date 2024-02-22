import logging

from django.contrib import auth
from django.contrib.contenttypes.models import ContentType
from rest_framework import status
from rest_framework.response import Response
from rest_framework.serializers import ValidationError
from rest_framework.views import APIView

from govapp.apps.accounts.serializers import UserKeyValueListSerializer

logger = logging.getLogger(__name__)


User = auth.get_user_model()


class AssignToMeAPIView(APIView):
    """An api end point that allows the request user to assign an object to themselves
    so long as the model the object is based on extends from AssignableModel

    Request type must be POST with parameters: content_type and object_id
    """

    def post(self, request, format=None):
        content_type = request.data.get("content_type", None)
        if not content_type:
            raise ValidationError("AssignToMeAPIView requires a content type")

        try:
            ContentType.objects.get(id=content_type)
        except ContentType.DoesNotExist:
            raise ValidationError(f"No content type found with id: {content_type}")

        object_id = request.data.get("object_id", None)
        if not object_id:
            raise ValidationError("AssignToMeAPIView requires an object id")

        model_class = ContentType.objects.get(id=content_type).model_class()

        try:
            instance = model_class.objects.get(id=object_id)
        except model_class.DoesNotExist:
            raise ValidationError(
                "No object found with content_type: {} and object_id: {}".format(
                    content_type, object_id
                )
            )

        if not instance.user_is_assignable(request.user):
            raise ValidationError(
                "You do not have permission to assign this object to yourself"
            )

        logger.info(
            f"Assigning: {instance._meta.object_name} {instance} to {request.user} (request user)"
        )

        instance.assign(request.user)

        logger.info(
            f"Assigned: {instance._meta.object_name} {instance} to {request.user} (request user)"
        )

        return Response({"user_id": request.user.id}, status=status.HTTP_200_OK)


class AssignableUsersAPIView(APIView):
    """An api end point that returns a list of users that can be assign to a model instance
      as the model the object is based on extends from AssignableModel

    Request type must be GET with parameters: content_type and object_id
    """

    def get(self, request, format=None):
        content_type = request.query_params.get("content_type", None)
        if not content_type:
            raise ValidationError("AssignableUsers requires a content type")

        try:
            ContentType.objects.get(id=content_type)
        except ContentType.DoesNotExist:
            raise ValidationError(f"No content type found with id: {content_type}")

        object_id = request.query_params.get("object_id", None)
        if not object_id:
            raise ValidationError("AssignableUsers requires an object id")

        model_class = ContentType.objects.get(id=content_type).model_class()

        try:
            instance = model_class.objects.get(id=object_id)
        except model_class.DoesNotExist:
            raise ValidationError(
                "No object found with content_type: {} and object_id: {}".format(
                    content_type, object_id
                )
            )

        assignable_users = instance.assignable_users()

        serializer = UserKeyValueListSerializer(assignable_users, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class AssignToAPIView(APIView):
    """An api end point that allows the request user to assign an object to themselves
    so long as the model the object is based on extends from AssignableModel

    Request type must be POST with parameters: content_type, object_id and user_id
    """

    def post(self, request, format=None):
        content_type = request.data.get("content_type", None)
        if not content_type:
            raise ValidationError("AssignToMeAPIView requires a content type")

        try:
            ContentType.objects.get(id=content_type)
        except ContentType.DoesNotExist:
            raise ValidationError(f"No content type found with id: {content_type}")

        object_id = request.data.get("object_id", None)
        if not object_id:
            raise ValidationError("AssignToMeAPIView requires an object id")

        model_class = ContentType.objects.get(id=content_type).model_class()

        try:
            instance = model_class.objects.get(id=object_id)
        except model_class.DoesNotExist:
            raise ValidationError(
                "No object found with content_type: {} and object_id: {}".format(
                    content_type, object_id
                )
            )

        if not instance.user_is_assignable(request.user):
            raise ValidationError(
                "You do not have permission to assign this object to yourself"
            )
        user_id = request.data.get("user_id", None)
        if not user_id:
            raise ValidationError("AssignToMeAPIView requires a user id")

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise ValidationError(f"No user found with id: {user_id}")

        logger.info(f"Assigning: {instance._meta.object_name} {instance} to {user}")

        instance.assign(user)

        logger.info(f"Assigned: {instance._meta.object_name} {instance} to {user}")

        return Response(status=status.HTTP_200_OK)
