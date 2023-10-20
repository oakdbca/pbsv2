from collections.abc import Iterable
from typing import Union

from django.conf import settings
from django.contrib import auth
from django.contrib.auth import models
from django.db.models import query

# Shortcuts
UserModel = auth.get_user_model()


def all_administrators() -> Iterable[models.User]:
    """Retrieves all of the administrator users.

    Yields:
        models.User: Users in the administrator group.
    """
    # Retrieve and Yield
    yield from UserModel.objects.filter(groups__id=settings.DJANGO_ADMIN)


def is_administrator(user: Union[models.User, models.AnonymousUser]) -> bool:
    """Checks whether a user is an Administrator.

    Args:
        user (Union[models.User, models.AnonymousUser]): User to be checked.

    Returns:
        bool: Whether the user is in the Administrator group.
    """
    # Check and Return
    return (
        not isinstance(user, models.AnonymousUser)  # Must be logged in
        and user.groups.filter(id=settings.DJANGO_ADMIN).exists()  # Must be in group
    )


def limit_to_administrators() -> query.Q:
    """Limits a fields choice to only objects in the Administrators group.

    Returns:
        query.Q: Query to limit object to those in the Administrators group.
    """
    # Construct Query and Return
    return query.Q(groups__pk=settings.DJANGO_ADMIN)
