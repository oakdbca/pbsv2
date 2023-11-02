from typing import Any

from django.contrib import admin
from django.http.request import HttpRequest

from .models import District, Lga, ModelFile, Region


class DeleteRestrictedAdmin(admin.ModelAdmin):
    def has_delete_permission(self, request: HttpRequest, obj=None):
        return request.user.is_superuser


class ModelFileAdmin(DeleteRestrictedAdmin):
    list_display = ("id", "file", "content_type", "object_id", "datetime_uploaded")


class RegionAdmin(DeleteRestrictedAdmin):
    list_display = ("id", "name", "display_name")

    def has_change_permission(
        self, request: HttpRequest, obj: Any | None = ...
    ) -> bool:
        return request.user.is_superuser


class DistrictAdmin(DeleteRestrictedAdmin):
    list_display = ("id", "region", "name", "display_name")

    def has_change_permission(
        self, request: HttpRequest, obj: Any | None = ...
    ) -> bool:
        return request.user.is_superuser


class LgaAdmin(DeleteRestrictedAdmin):
    list_display = ("id", "district", "name", "display_name")

    def has_change_permission(
        self, request: HttpRequest, obj: Any | None = ...
    ) -> bool:
        return request.user.is_superuser


admin.site.register(ModelFile, ModelFileAdmin)
admin.site.register(Region, RegionAdmin)
admin.site.register(District, DistrictAdmin)
admin.site.register(Lga, LgaAdmin)
