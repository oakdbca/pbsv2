import logging

from django.conf import settings
from django.contrib.auth.models import Group
from django.core.cache import cache

logger = logging.getLogger(__name__)


def cached_groups():
    # Try to get groups from cache
    groups = cache.get("groups")

    # If groups are not in cache, fetch them from the database and store them in cache
    if groups is None:
        groups = Group.objects.all()
        cache.set("groups", groups)

    return groups


def is_member_of(user, group_name):
    groups = cached_groups()
    if not groups.filter(name=group_name).exists():
        logger.warning(f"Group {group_name} does not exist")
        return False
    return (
        user.is_superuser or user.profile.cached_groups.filter(name=group_name).exists()
    )


def is_internal(user):
    return user.is_superuser or user.is_staff


def is_django_admin(user):
    return is_member_of(user, settings.DJANGO_ADMIN)
