"""Django settings for the Prescribed Burns System project.

Generated by `django-admin startproject` using Django 3.2.16.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

import hashlib
import json
import os
import pathlib
import platform
from typing import Any

import decouple
import dj_database_url
import tomli

DEBUG = decouple.config("DEBUG", default=False, cast=bool)
ENVIRONMENT = decouple.config("ENVIRONMENT", default="dev")

if DEBUG is True and ENVIRONMENT == "local":
    import django_stubs_ext

    django_stubs_ext.monkeypatch()

# Build paths inside the project like this: BASE_DIR / "subdir".
BASE_DIR = pathlib.Path(__file__).resolve().parent.parent
project = tomli.load(open(os.path.join(BASE_DIR, "pyproject.toml"), "rb"))

APPLICATION_VERSION = project["tool"]["poetry"]["version"]

# Sentry settings
SENTRY_DSN = decouple.config("SENTRY_DSN", default=None)
SENTRY_SAMPLE_RATE = decouple.config(
    "SENTRY_SAMPLE_RATE", default=1.0, cast=float
)  # Error sampling rate
SENTRY_TRANSACTION_SAMPLE_RATE = decouple.config(
    "SENTRY_TRANSACTION_SAMPLE_RATE", default=0.0, cast=float
)  # Transaction sampling
ENVIRONMENT = decouple.config("ENVIRONMENT", default=None)
if SENTRY_DSN and ENVIRONMENT:
    import sentry_sdk

    sentry_sdk.init(
        dsn=SENTRY_DSN,
        sample_rate=SENTRY_SAMPLE_RATE,
        traces_sample_rate=SENTRY_TRANSACTION_SAMPLE_RATE,
        environment=ENVIRONMENT,
        release=APPLICATION_VERSION,
    )

STATIC_ROOT = BASE_DIR / "staticfiles"

# Project specific settings
PROJECT_TITLE = "Bushfire Mitigation System"
PROJECT_DESCRIPTION = (
    "A system to manage risk, planning, implementation and post-implementation "
    "review for the mitigation of bushfires in Western Australia"
)
PROJECT_VERSION = "v2"

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/
# SECURITY WARNING: keep the secret key used in production secret!
# SECURITY WARNING: don't run with debug turned on in production!
# SECURITY WARNING: don't allow all hosts in production!
SECRET_KEY = decouple.config("SECRET_KEY")
ALLOWED_HOSTS = [""]
if DEBUG is True:
    ALLOWED_HOSTS = ["*"]
    CSRF_TRUSTED_ORIGINS = ["https://*.dbca.wa.gov.au"]
else:
    ALLOWED_HOSTS_STRING = decouple.config("ALLOWED_HOSTS", default='[""]')
    CSRF_TRUSTED_ORIGINS = decouple.config("CSRF_TRUSTED_ORIGINS", default='[""]')
    ALLOWED_HOSTS = json.loads(ALLOWED_HOSTS_STRING)

# Application definition
INSTALLED_APPS = [
    "reversion",
    "django.contrib.auth",
    "django.contrib.admin",
    "django.contrib.contenttypes",
    "django.contrib.gis",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "corsheaders",
    "webtemplate_dbca",
    "govapp",
    "govapp.apps.accounts",
    "govapp.apps.actions",
    "govapp.apps.aviation",
    "govapp.apps.burnplanning",
    "govapp.apps.legalapproval",
    "govapp.apps.operationalplanning",
    "govapp.apps.prescriptiondetails",
    "govapp.apps.risk",
    "govapp.apps.swagger",
    "govapp.apps.traffic",
    "govapp.apps.main",
    "rest_framework",
    "rest_framework_datatables",
    "rest_framework_gis",
    "drf_spectacular",
    "django_filters",
    "django_cron",
    "django_extensions",
    "coverage",
    "protected_media.apps.ProtectedMediaConfig",
    "nested_admin",
    "drf_standardized_errors",
]
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "dbca_utils.middleware.SSOLoginMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "govapp.middleware.CacheControl",
]
ROOT_URLCONF = "govapp.urls"
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            BASE_DIR / "govapp/templates",
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "govapp.context_processors.variables",
            ],
        },
    },
]
WSGI_APPLICATION = "govapp.wsgi.application"

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases
DATABASES = {
    "default": decouple.config(
        "DATABASE_URL", cast=dj_database_url.parse, default="sqlite://memory"
    ),
    "test": decouple.config(
        "TEST_DATABASE_URL", cast=dj_database_url.parse, default="sqlite://memory"
    ),
}

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/
LANGUAGE_CODE = "en-au"
# TIME_ZONE = "UTC"
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/
STATIC_URL = "/static/"
STATICFILES_DIRS = [
    os.path.join(os.path.join(BASE_DIR, "govapp", "static")),
]

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Caching settings
# https://docs.djangoproject.com/en/3.2/ref/settings/#caches
USE_DUMMY_CACHE = decouple.config("USE_DUMMY_CACHE", False, cast=bool)
if USE_DUMMY_CACHE:
    CACHES = {
        "default": {
            "BACKEND": "django.core.cache.backends.dummy.DummyCache",
        },
    }
else:
    CACHES = {
        "default": {
            "BACKEND": "django.core.cache.backends.filebased.FileBasedCache",
            "LOCATION": os.path.join(BASE_DIR, "govapp", "cache"),
        },
    }

# DBCA Template Settings
# https://github.com/dbca-wa/django-base-template/blob/main/govapp/settings.py
ENABLE_DJANGO_LOGIN = decouple.config("ENABLE_DJANGO_LOGIN", default=False, cast=bool)
LEDGER_TEMPLATE = "bootstrap5"
GIT_COMMIT_HASH = os.popen(
    f"cd {BASE_DIR}; git log -1 --format=%H"
).read()  # noqa: S605
GIT_COMMIT_DATE = os.popen(
    f"cd {BASE_DIR}; git log -1 --format=%cd"
).read()  # noqa: S605
VERSION_NO = "2.00"

if DEBUG:
    rest_framework_renderer_classes = [
        "rest_framework.renderers.JSONRenderer",
        "rest_framework.renderers.BrowsableAPIRenderer",
        "rest_framework_datatables.renderers.DatatablesRenderer",
    ]
else:
    rest_framework_renderer_classes = [
        "rest_framework.renderers.JSONRenderer",
        "rest_framework_datatables.renderers.DatatablesRenderer",
    ]

# Django REST Framework Settings
# https://www.django-rest-framework.org/api-guide/settings/
REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "DEFAULT_RENDERER_CLASSES": rest_framework_renderer_classes,
    "DEFAULT_FILTER_BACKENDS": [
        "django_filters.rest_framework.DjangoFilterBackend",
        "rest_framework.filters.SearchFilter",
    ],
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.LimitOffsetPagination",
    "PAGE_SIZE": 100,
    "EXCEPTION_HANDLER": "drf_standardized_errors.handler.exception_handler",
}

# DRF Spectacular Settings
# https://drf-spectacular.readthedocs.io/en/latest/settings.html
SPECTACULAR_SETTINGS = {
    "TITLE": PROJECT_TITLE,
    "DESCRIPTION": PROJECT_DESCRIPTION,
    "VERSION": PROJECT_VERSION,
    "SERVE_INCLUDE_SCHEMA": True,
    "POSTPROCESSING_HOOKS": [],
    "COMPONENT_SPLIT_REQUEST": True,
}

# Logging
# https://docs.djangoproject.com/en/3.2/topics/logging/
LOGGING: dict[str, Any] = {
    "version": 1,
    "disable_existing_loggers": True,
    "formatters": {
        "verbose": {
            "format": "%(levelname)s %(asctime)s %(name)s [Line:%(lineno)s][%(funcName)s] %(message)s"
        },
        "simple": {"format": "%(levelname)s %(message)s"},
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "DEBUG",
            "formatter": "verbose",
        },
        "console_simple": {
            "class": "logging.StreamHandler",
            "level": "DEBUG",
            "formatter": "simple",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "INFO",
    },
    "loggers": {
        "govapp": {
            "handlers": ["console"],
            "level": "INFO",
        },
    },
}

if DEBUG is True:
    LOGGING["loggers"]["govapp"]["handlers"] = ["console_simple"]
    LOGGING["loggers"]["govapp"]["level"] = "DEBUG"
    LOGGING["loggers"]["govapp"]["propagate"] = False


# Email
DISABLE_EMAIL = decouple.config("DISABLE_EMAIL", default=False, cast=bool)
BUILD_TAG = decouple.config(
    "BUILD_TAG", hashlib.sha256(os.urandom(64)).hexdigest()
)  # URL of the Dev app.js served by webpack & express

# EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_BACKEND = "wagov_utils.components.utils.email_backend.EmailBackend"
EMAIL_HOST = decouple.config("EMAIL_HOST", default="smtp.lan.fyi")
EMAIL_PORT = decouple.config("EMAIL_PORT", default=25, cast=int)
DEFAULT_FROM_EMAIL = "no-reply@dbca.wa.gov.au"
EMAIL_INSTANCE = decouple.config("EMAIL_INSTANCE", default="PROD")
NON_PROD_EMAIL = decouple.config("NON_PROD_EMAIL", default="")
PRODUCTION_EMAIL = decouple.config("PRODUCTION_EMAIL", default=False, cast=bool)
EMAIL_DELIVERY = decouple.config("EMAIL_DELIVERY", default="off")

# Django Cron
CRON_SCANNER_PERIOD_MINS = 5  # Run every 5 minutes
CRON_CLASSES: list[str] = []

# Django debug toolbar
SHOW_DEBUG_TOOLBAR = decouple.config("SHOW_DEBUG_TOOLBAR", default=False, cast=bool)
if SHOW_DEBUG_TOOLBAR:

    def show_toolbar(request):
        if request:
            return True

    MIDDLEWARE += [
        "debug_toolbar.middleware.DebugToolbarMiddleware",
    ]
    INSTALLED_APPS += ("debug_toolbar",)
    INTERNAL_IPS = ("127.0.0.1", "localhost", "internalhost", "externalhost")

    # this dict removes check to dtermine if toolbar should display --> works for rks docker container
    DEBUG_TOOLBAR_CONFIG = {
        # "SHOW_TOOLBAR_CALLBACK": show_toolbar,
        "INTERCEPT_REDIRECTS": False,
    }

# Compress static files
STATICFILES_STORAGE = "whitenoise.storage.CompressedStaticFilesStorage"

# Temporary Fix for ARM Architecture
if platform.machine() == "arm64":
    GDAL_LIBRARY_PATH = "/opt/homebrew/opt/gdal/lib/libgdal.dylib"
    GEOS_LIBRARY_PATH = "/opt/homebrew/opt/geos/lib/libgeos_c.dylib"


# Django Timezone
TIME_ZONE = "Australia/Perth"

# GIS Server
GIS_SERVER_URL = decouple.config("GIS_SERVER_URL", default="https://kmi.dbca.wa.gov.au")

GOV_APPS = [
    app.replace("govapp.apps.", "")
    for app in INSTALLED_APPS
    if app.startswith("govapp.apps.")
]
GOV_APPS.remove("main")

EXCLUDE_GRAPH_MODELS = [
    "UniqueNameableModel",
    "NameableModel",
    "NullableNameableModel",
    "DisplayNameableModel",
    "OrdinalScaleModel",
    "LodgementDateModel",
    "ReferenceableModel",
    "AssignableModel",
    "ArchivableModel",
    "DocumentCategory",
    "DocumentDescriptor",
    "ModelFile",
    "TimeStampedModel",
    "ContentType",
]

GRAPH_MODELS = {"app_labels": GOV_APPS, "exclude_models": EXCLUDE_GRAPH_MODELS}

# Protected Media
PROTECTED_MEDIA_ROOT = "%s/protected/" % BASE_DIR
PROTECTED_MEDIA_URL = "/protected"
if DEBUG is False:
    PROTECTED_MEDIA_SERVER = "nginx"  # Defaults to "django"
PROTECTED_MEDIA_LOCATION_PREFIX = "/internal"  # Prefix used in nginx config
PROTECTED_MEDIA_AS_DOWNLOADS = (
    False  # Controls inclusion of a Content-Disposition header
)

# Todo do we need this?
AZURE_OUTPUT_SYNC_DIRECTORY = ""

SEASON_CHOICES = (
    ("autumn", "Autumn"),
    ("winter", "Winter"),
    ("spring", "Spring"),
    ("summer", "Summer"),
)

# Groups

DJANGO_ADMIN = "Django Admin"

CORPORATE_EXECUTIVE = "Corporate Executive"
DISTRICT_DUTY_OFFICER = "District Duty Officer"
DISTRICT_FIRE_COORDINATOR = "District Fire Coordinator"
DISTRICT_MANAGER = "District Manager"
DJANGO_ADMIN = "Django Admin"
FMSB_REPRESENTATIVE = "FMSB Representative"
OFFICER = "Officer"
REGIONAL_DUTY_OFFICER = "Regional Duty Officer"
REGIONAL_LEADER_FIRE = "Regional Leader Fire"
REGIONAL_MANAGER = "Regional Manager"
SCHEDULER = "Scheduler"
STATE_AVIATION = "State Aviation"
STATE_DUTY_OFFICER = "State Duty Officer"
STATE_MANAGER = "State Manager"

DJANGO_GROUPS = [
    CORPORATE_EXECUTIVE,
    DISTRICT_DUTY_OFFICER,
    DISTRICT_FIRE_COORDINATOR,
    DISTRICT_MANAGER,
    DJANGO_ADMIN,
    FMSB_REPRESENTATIVE,
    OFFICER,
    REGIONAL_DUTY_OFFICER,
    REGIONAL_LEADER_FIRE,
    REGIONAL_MANAGER,
    SCHEDULER,
    STATE_AVIATION,
    STATE_DUTY_OFFICER,
    STATE_MANAGER,
    DJANGO_ADMIN,
]

# Configure CKEditor 5
CKEDITOR_CONFIGS = {
    "default": {
        "toolbar": "full",
        "height": 300,
        "width": "100%",
    },
    "awesome_ckeditor": {
        "toolbar": "Basic",
    },
    "toolbar_minimal": {
        "toolbar": "Custom",
        "toolbar_Custom": [
            ["Bold", "Italic", "Underline"],
            [
                "BulletedList",
                "NumberedList",
                "-",
                "Outdent",
                "Indent",
                "-",
                "Image",
                "Blockquote",
                "Table",
                "MediaEmbed",
                "-",
                "Undo",
                "Redo",
                "-",
                "JustifyLeft",
                "JustifyCenter",
                "JustifyRight",
                "JustifyBlock",
            ],
            ["Link", "Unlink"],
            ["RemoveFormat", "Source"],
        ],
    },
}
