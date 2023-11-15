from django.contrib import admin

from govapp.apps.main.admin import DeleteRestrictedAdmin

from .models import ContributingFactor, RiskCategory


@admin.register(ContributingFactor)
class ContributingFactorAdmin(DeleteRestrictedAdmin):
    model = ContributingFactor
    list_display = (
        "name",
        "factors",
    )


@admin.register(RiskCategory)
class RiskCategoryAdmin(DeleteRestrictedAdmin):
    model = RiskCategory
    list_display = ("name",)
