import logging

from django.conf import settings
from django.contrib.auth.models import Group

logger = logging.getLogger(__name__)


def is_member_of(user, group_name):
    # Todo: Consider caching the groups
    if not Group.objects.filter(name=group_name).exists():
        logger.warning(f"Group {group_name} does not exist")
        return False
    return user.is_superuser or user.groups.filter(name=group_name).exists()


def is_internal(user):
    return user.is_superuser or user.is_staff


def is_django_admin(user):
    return is_member_of(settings.DJANGO_ADMIN)
