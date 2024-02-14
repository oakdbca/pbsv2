"""Prescribed Burns System URL Configuration.

The `urlpatterns` list routes URLs to views.
For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/

Examples:
    Function views
        1. Add an import:  from my_app import views
        2. Add a URL to urlpatterns:  path("", views.home, name="home")
    Class-based views
        1. Add an import:  from other_app.views import Home
        2. Add a URL to urlpatterns:  path("", Home.as_view(), name="home")
    Including another URLconf
        1. Import the include() function: from django.urls import include, path
        2. Add a URL to urlpatterns:  path("blog/", include("blog.urls"))
"""


# Third-Party
from django import conf, urls
from django.contrib import admin
from django.contrib.auth import views as auth_views
from rest_framework import routers

# Local
from govapp import views

# Admin Site Settings
admin.site.site_header = conf.settings.PROJECT_TITLE
admin.site.index_title = conf.settings.PROJECT_TITLE
admin.site.site_title = conf.settings.PROJECT_TITLE


# To test sentry
def trigger_error(request):
    division_by_zero = 1 / 0  # noqa


router = routers.DefaultRouter()
router.registry.sort(key=lambda x: x[0])

# Django URL Patterns
urlpatterns = [
    # Home Page
    urls.path("", views.HomePage.as_view(), name="home"),
    urls.path("test", views.HomePage.as_view(), name="test"),
    urls.path("burnplanning", views.HomePage.as_view(), name="burnplanning"),
    # Protected media
    urls.path("protected/", urls.include("protected_media.urls")),
    # Django Administration
    urls.path("admin/", admin.site.urls),
    urls.path("sentry-debug/", trigger_error),
    # Include urls from other apps
    urls.path("", urls.include("govapp.apps.burnplanning.urls")),
    urls.path("", urls.include("govapp.apps.main.urls")),
    urls.path("", urls.include("govapp.apps.swagger.urls")),
    # Include API routes
    urls.path("api/", urls.include(router.urls)),
]

# DBCA Template URLs
urlpatterns.append(
    urls.path(
        "logout/", auth_views.LogoutView.as_view(), {"next_page": "/"}, name="logout"
    )
)
if conf.settings.ENABLE_DJANGO_LOGIN:
    urlpatterns.append(
        urls.re_path(r"^ssologin/", auth_views.LoginView.as_view(), name="ssologin")
    )
