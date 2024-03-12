from typing import Any, Optional

from django.conf import settings
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from django.db.models.query import QuerySet
from django.http import HttpRequest

from govapp.apps.accounts.models import Profile


# Define an inline admin descriptor for Employee model
# which acts a bit like a singleton
class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False


# Define a new User admin
class UserAdmin(BaseUserAdmin):
    inlines = [ProfileInline]

    def has_change_permission(
        self, request: HttpRequest, obj: User | None = None
    ) -> bool:
        if obj and obj.username == settings.PROJECT_TITLE:
            return False
        return super().has_change_permission(request, obj)

    def has_delete_permission(
        self, request: HttpRequest, obj: User | None = None
    ) -> bool:
        if obj and obj.username == settings.PROJECT_TITLE:
            return False
        return super().has_delete_permission(request, obj)

    def save_model(
        self, request: HttpRequest, obj: User, form: Optional[Any], change: bool
    ) -> None:
        if obj.username == settings.PROJECT_TITLE:
            return
        return super().save_model(request, obj, form, change)

    def delete_model(self, request: HttpRequest, obj: Any) -> None:
        if obj.username == settings.PROJECT_TITLE:
            return
        return super().delete_model(request, obj)

    def delete_queryset(self, request: HttpRequest, queryset: QuerySet[Any]) -> None:
        queryset.exclude(username=settings.PROJECT_TITLE)
        return super().delete_queryset(request, queryset)


# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
