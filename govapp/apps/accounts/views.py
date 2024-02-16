# Third-Party
from django.contrib import auth
from django.contrib.auth import models
from drf_spectacular import utils
from rest_framework import decorators, request, response, viewsets

# Local
from govapp.apps.accounts import filters, serializers
from govapp.permissions import IsDjangoAdmin, IsPBSAdmin

# Shortcuts
UserModel = auth.get_user_model()
GroupModel = models.Group


@utils.extend_schema(tags=["Accounts - Users"])
class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """User View Set."""

    queryset = UserModel.objects.all()
    serializer_class = serializers.UserSerializer
    filterset_class = filters.UserFilter
    permission_classes = [IsPBSAdmin | IsDjangoAdmin]

    @utils.extend_schema(request=None, responses=serializers.UserProfileSerializer)
    @decorators.action(detail=False, methods=["GET"])
    def me(self, request: request.Request) -> response.Response:
        """Retrieves the currently logged in user (including their profile and groups)

        Args:
            request (request.Request): API request.

        Returns:
            response.Response: The currently logged in user if applicable.
        """
        # Retrieve User
        instance = request.user

        # Serialize User
        serializer = serializers.UserProfileSerializer(instance)

        # Return Response
        return response.Response(serializer.data)


@utils.extend_schema(tags=["Accounts - Groups"])
class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    """Group View Set."""

    queryset = GroupModel.objects.all()
    serializer_class = serializers.GroupSerializer

    @utils.extend_schema(request=None, responses=serializers.GroupSerializer)
    @decorators.action(detail=False, methods=["GET"])
    def mine(self, request: request.Request) -> response.Response:
        """Retrieves the groups for the currently logged in user

        Args:
            request (request.Request): API request.

        Returns:
            response.Response: The currently logged in user if applicable.
        """
        # Serialize User
        serializer = self.get_serializer(request.user.groups, many=True)

        # Return Response
        return response.Response(serializer.data)
