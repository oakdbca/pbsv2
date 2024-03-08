import logging

from django.conf import settings
from django.contrib import auth
from django.contrib.auth.models import Group
from django.core.cache import cache

logger = logging.getLogger(__name__)

User = auth.get_user_model()


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


def is_pbs_admin(user):
    return is_member_of(user, settings.PBS_ADMIN)


def get_model_by_reference_number(reference_number):
    model_prefix = "".join([c for c in reference_number if c.isupper()])
    logger.debug(f"Model prefix: {model_prefix}")
    return get_model_by_model_prefix(model_prefix)


def get_model_by_model_prefix(prefix):
    """A bit annoying to have to use this however when using union
    all the instances in a queryset are cast to one model type so it's
    seemingly impossible to generate a details url for the real instance type."""
    from django.apps import apps

    for model in apps.get_models():
        if hasattr(model, "MODEL_PREFIX") and model.MODEL_PREFIX == prefix:
            return model
    return None
