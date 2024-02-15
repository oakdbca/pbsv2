import logging

from rest_framework.permissions import BasePermission

from govapp.helpers import is_internal

logger = logging.getLogger(__name__)


class IsInternal(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True
        if is_internal(request.user):
            if "DELETE" == request.method:
                return False

            return True
        return False
