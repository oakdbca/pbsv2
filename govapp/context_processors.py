# Third-Party
from django import conf
from django.core.cache import cache


def variables(request):  # (request: http.HttpRequest) -> dict[str, Any]:
    """Constructs a context dictionary to be passed to the templates.

    Args:
        request (http.HttpRequest): HTTP request object.

    Returns:
        dict[str, Any]: Context for the templates.
    """
    # Construct and return context
    is_django_admin = False
    is_admin = False

    if request.session.session_key is not None:
        is_django_admin = cache.get(
            "is_django_admin" + str(request.session.session_key)
        )
        is_admin = cache.get("is_admin" + str(request.session.session_key))

        if is_django_admin is None:
            try:
                is_django_admin = request.user.groups.filter(
                    name="Django Admin"
                ).exists()
            except Exception as e:
                print(e)
            cache.set(
                "is_django_admin" + str(request.session.session_key),
                is_django_admin,
                86400,
            )
        if is_admin is None:
            try:
                is_admin = request.user.groups.filter(name="Administrators").exists()
            except Exception as e:
                print(e)

            cache.set("is_admin" + str(request.session.session_key), is_admin, 86400)

    return {
        "template_group": "pbs",
        "template_title": "",
        "build_tag": conf.settings.BUILD_TAG,
        "GIT_COMMIT_HASH": conf.settings.GIT_COMMIT_HASH,
        "DJANGO_SETTINGS": conf.settings,
        "settings": conf.settings,
        "is_django_admin": is_django_admin,  # request.user.groups.filter(name="Django Admin").exists(),
        "is_admin": is_admin,  # request.user.groups.filter(name="Administrators").exists(),
    }
