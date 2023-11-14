from django.contrib import admin

from govapp.apps.traffic.models import Road


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
