import nested_admin
from django import forms
from django.contrib import admin

from govapp.apps.main.admin import NestedDeleteRestrictedAdmin
from govapp.apps.traffic.models import (
    Road,
    RoadOwner,
    Traffic,
    TrafficGuidanceScheme,
    TrafficRequiredArrangement,
)


@admin.register(TrafficGuidanceScheme)
class TrafficGuidanceSchemeAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "display_name",
        "active_from",
        "active_to",
        "hyperlink",
    )

    search_fields = (
        "name",
        "display_name",
        "active_from",
        "active_to",
        "hyperlink",
    )
    ordering = ("name",)


class TrafficGuidanceSchemeForm(forms.ModelForm):
    class Meta:
        model = TrafficGuidanceScheme
        fields = "__all__"
        help_texts = {
            "active_from": "Assigned from the active-period of the linked document",
            "active_to": "Assigned from the active-period of the linked document",
            "hyperlink": "The Traffic Guidance Scheme PDF document",
        }


@admin.register(RoadOwner)
class RoadOwnerAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)
    ordering = ("name",)


class RoadInline(nested_admin.NestedStackedInline):
    model = Road
    extra = 0

    class Media:
        css = {
            "all": ["admin/class_media/css/inline_fieldsets.css"],
        }

    list_display = (
        "id",
        "name",
        "display_name",
        "owner",
        "speed",
        "shoulder_width",
    )

    fieldsets = (
        (
            None,
            {
                "fields": (
                    (
                        "name",
                        "display_name",
                    ),
                    ("owner",),
                    (
                        "speed",
                        "shoulder_width",
                    ),
                ),
                "classes": (
                    "less-dominant-style",
                    "nested-inline-flex-container",
                ),
            },
        ),
    )


@admin.register(TrafficRequiredArrangement)
class TrafficRequiredArrangementAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "traffic_guidance_scheme",
        "date_of_installation",
    )
    search_fields = ("display_name",)

    ordering = ("date_of_installation",)
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "traffic_guidance_scheme",
                    "map_pin",
                    "date_of_installation",
                    "traffic",
                ),
            },
        ),
    )

    readonly_fields = ("traffic",)


class TrafficRequiredArrangementInline(nested_admin.NestedStackedInline):
    model = TrafficRequiredArrangement
    extra = 0

    class Media:
        css = {
            "all": ["admin/class_media/css/inline_fieldsets.css"],
        }

    list_display = (
        "id",
        "traffic_guidance_scheme",
        "date_of_installation",
    )

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "traffic_guidance_scheme",
                    "map_pin",
                    "date_of_installation",
                    "traffic",
                ),
            },
        ),
    )

    readonly_fields = ("traffic",)


@admin.register(Road)
class RoadAdmin(NestedDeleteRestrictedAdmin):
    list_display = (
        "id",
        "name",
        "display_name",
        "owner",
        "speed",
        "shoulder_width",
    )
    search_fields = (
        "name",
        "display_name",
        "owner",
        "speed",
        "shoulder_width",
    )
    ordering = ("name",)


@admin.register(Traffic)
class TrafficAdmin(NestedDeleteRestrictedAdmin):
    list_display = (
        "id",
        "name",
        "display_name",
        "indicative_traffic_management_scheme",
    )
    search_fields = (
        "name",
        "display_name",
    )
    ordering = ("name",)

    class Media:
        css = {
            "all": ["admin/class_media/css/inline_fieldsets.css"],
        }

    fieldsets = (
        (
            None,
            {
                "fields": (
                    (
                        "name",
                        "display_name",
                    ),
                    ("indicative_traffic_management_scheme",),
                    "roads",
                ),
                "classes": (
                    "less-dominant-style",
                    "nested-inline-flex-container",
                ),
            },
        ),
    )

    inlines = [TrafficRequiredArrangementInline]
