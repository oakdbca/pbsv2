from django.contrib import admin

from govapp.apps.traffic.models import Road, RoadOwner, TrafficGuidanceScheme


@admin.register(TrafficGuidanceScheme)
class TrafficGuidanceSchemeAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "display_name",
        "road",
        "active_from",
        "active_to",
        "hyperlink",
    )
    list_filter = ("road",)
    search_fields = (
        "name",
        "display_name",
        "road",
        "active_from",
        "active_to",
        "hyperlink",
    )
    ordering = ("name",)


@admin.register(RoadOwner)
class RoadOwnerAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)
    ordering = ("name",)


@admin.register(Road)
class RoadAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "display_name",
        "traffic",
        "owner",
        "speed",
        "shoulder_width",
    )
    list_filter = ("traffic",)
    search_fields = (
        "name",
        "display_name",
        "traffic",
        "owner",
        "speed",
        "shoulder_width",
    )
    ordering = ("name",)
