import logging

from django.conf import settings
from rest_framework.permissions import BasePermission

from govapp.helpers import is_internal, is_member_of

logger = logging.getLogger(__name__)


class IsInternal(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        if request.user.is_superuser:
            return True
        if is_internal(request.user):
            if "DELETE" == request.method:
                return False

            return True
        return False


class IsDjangoAdmin(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        if request.user.is_superuser:
            return True
        return is_member_of(request.user, settings.DJANGO_ADMIN)


class IsPBSAdmin(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        if request.user.is_superuser:
            return True
        return is_member_of(request.user, settings.PBS_ADMIN)


class HasObjectPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True
        return obj.has_object_permission(request.user)
