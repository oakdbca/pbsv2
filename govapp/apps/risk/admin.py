from django.contrib import admin

from govapp.apps.main.admin import DeleteRestrictedAdmin

from .models import (
    ContributingFactor,
    ContributingFactorStandardControl,
    RiskCategory,
    StandardControl,
)


@admin.register(StandardControl)
class StandardControlAdmin(DeleteRestrictedAdmin):
    model = StandardControl
    list_display = ("name",)


class ContributingFactorStandardControlInline(admin.TabularInline):
    model = ContributingFactorStandardControl
    extra = 0


@admin.register(ContributingFactor)
class ContributingFactorAdmin(DeleteRestrictedAdmin):
    model = ContributingFactor
    list_display = (
        "name",
        "factors",
    )

    inlines = [
        ContributingFactorStandardControlInline,
    ]


@admin.register(RiskCategory)
class RiskCategoryAdmin(DeleteRestrictedAdmin):
    model = RiskCategory
    list_display = ("name",)
