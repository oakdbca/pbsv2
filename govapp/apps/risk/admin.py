from django.contrib import admin

from govapp.apps.main.admin import DeleteRestrictedAdmin

from .models import ContributingFactor, RiskFactor


@admin.register(ContributingFactor)
class ContributingFactorAdmin(DeleteRestrictedAdmin):
    model = ContributingFactor
    list_display = (
        "name",
        "factors",
    )


@admin.register(RiskFactor)
class RiskFactorAdmin(DeleteRestrictedAdmin):
    model = RiskFactor
    list_display = ("name",)
