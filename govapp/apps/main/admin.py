from typing import Any

import nested_admin
from django.contrib import admin
from django.http.request import HttpRequest

from .models import (
    District,
    DocumentCategory,
    DocumentDescriptor,
    Lga,
    ModelFile,
    Neighbour,
    NeighbourRole,
    Region,
)


class DeleteRestrictedAdmin(admin.ModelAdmin):
    def has_delete_permission(self, request: HttpRequest, obj=None):
        return request.user.is_superuser


class NestedDeleteRestrictedAdmin(nested_admin.NestedModelAdmin):
    def has_delete_permission(self, request: HttpRequest, obj=None):
        return request.user.is_superuser


class DocumentCategoryAdmin(DeleteRestrictedAdmin):
    list_display = ("id", "name")


class DocumentDescriptorAdmin(DeleteRestrictedAdmin):
    list_display = ("id", "name")


class ModelFileAdmin(DeleteRestrictedAdmin):
    list_display = (
        "id",
        "category",
        "descriptor",
        "file",
        "content_type",
        "object_id",
        "datetime_uploaded",
    )


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
    list_display = ("id", "name", "display_name")

    def has_change_permission(
        self, request: HttpRequest, obj: Any | None = ...
    ) -> bool:
        return request.user.is_superuser


class NeighbourRoleAdmin(DeleteRestrictedAdmin):
    list_display = ("id", "name")

    def has_change_permission(
        self, request: HttpRequest, obj: Any | None = ...
    ) -> bool:
        return request.user.is_superuser


class NeighbourAdmin(DeleteRestrictedAdmin):
    list_display = ("id", "name", "phone", "role", "location")

    def has_change_permission(
        self, request: HttpRequest, obj: Any | None = ...
    ) -> bool:
        return request.user.is_superuser


admin.site.register(DocumentDescriptor, DocumentDescriptorAdmin)
admin.site.register(DocumentCategory, DocumentCategoryAdmin)
admin.site.register(ModelFile, ModelFileAdmin)
admin.site.register(Region, RegionAdmin)
admin.site.register(District, DistrictAdmin)
admin.site.register(Lga, LgaAdmin)
admin.site.register(NeighbourRole, NeighbourRoleAdmin)
admin.site.register(Neighbour, NeighbourAdmin)
