from django.contrib import admin

from govapp.apps.main.admin import NestedDeleteRestrictedAdmin
from govapp.apps.prescriptiondetails.models import FuelType


@admin.register(FuelType)
class FuelTypeAdmin(NestedDeleteRestrictedAdmin):
    model = FuelType
    list_display = ("name",)
