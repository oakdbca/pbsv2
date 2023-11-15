import nested_admin
from django import forms
from django.contrib import admin

from govapp.apps.main.admin import NestedDeleteRestrictedAdmin
from govapp.apps.traffic.models import Road, RoadOwner, Traffic, TrafficGuidanceScheme


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


class TrafficGuidanceSchemeForm(forms.ModelForm):
    class Meta:
        model = TrafficGuidanceScheme
        fields = "__all__"
        help_texts = {
            "active_from": "Assigned from the active-period of the linked document",
            "active_to": "Assigned from the active-period of the linked document",
            "hyperlink": "The Traffic Guidance Scheme PDF document",
        }


class TrafficGuidanceSchemeInline(nested_admin.NestedStackedInline):
    model = TrafficGuidanceScheme
    extra = 0
    form = TrafficGuidanceSchemeForm

    class Media:
        css = {
            "all": ["admin/class_media/css/inline_fieldsets.css"],
        }

    list_display = (
        "id",
        "name",
        "display_name",
        "active_from",
        "active_to",
        "hyperlink",
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
                    (
                        "active_from",
                        "active_to",
                    ),
                    "hyperlink",
                ),
                "classes": (
                    "less-dominant-style",
                    "nested-inline-flex-container",
                ),
            },
        ),
    )


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
        "traffic",
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
                    (
                        "traffic",
                        "owner",
                    ),
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

    inlines = [TrafficGuidanceSchemeInline]


@admin.register(Road)
class RoadAdmin(NestedDeleteRestrictedAdmin):
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

    inlines = [TrafficGuidanceSchemeInline]


@admin.register(Traffic)
class TrafficAdmin(NestedDeleteRestrictedAdmin):
    list_display = ("id", "name", "display_name")
    search_fields = ("name", "display_name", "indicative_traffic_management_scheme")
    ordering = ("name",)

    inlines = [RoadInline]
