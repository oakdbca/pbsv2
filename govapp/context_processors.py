# Third-Party
from typing import Any

from django import conf, http


def variables(requestrequest: http.HttpRequest) -> dict[str, Any]:
    """Constructs a context dictionary to be passed to the templates.

    Args:
        request (http.HttpRequest): HTTP request object.

    Returns:
        dict[str, Any]: Context for the templates.
    """

    return {
        "template_group": "pbs",
        "template_title": "",
        "build_tag": conf.settings.BUILD_TAG,
        "GIT_COMMIT_HASH": conf.settings.GIT_COMMIT_HASH,
        "GIS_SERVER_URL": conf.settings.GIS_SERVER_URL,
        "DJANGO_SETTINGS": conf.settings,
        "settings": conf.settings,
    }
