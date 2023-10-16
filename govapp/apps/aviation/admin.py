from django.contrib import admin
from django.contrib.contenttypes.admin import GenericStackedInline

from govapp.apps.main.admin import DeleteRestrictedAdmin
from govapp.apps.main.models import ModelFile

from .models import AircraftRegistration, AircraftType, AviationRequest, IgnitionMethod


class IgnitionMethodAdmin(DeleteRestrictedAdmin):
    pass


class AircraftTypeAdmin(DeleteRestrictedAdmin):
    pass


class AircraftRegistrationAdmin(DeleteRestrictedAdmin):
    pass


class ModelFileInline(GenericStackedInline):
    model = ModelFile
    extra = 0
    verbose_name = "Decision File"


class AviationRequestAdmin(DeleteRestrictedAdmin):
    list_display = (
        "reference_number",
        "status",
        "ignition_method",
        "aircraft_type",
        "aircraft_registration",
        "datetime_requested",
        "duration",
        "assigned_to",
        "decision_made_by",
        "decision_datetime",
    )
    inlines = [ModelFileInline]


admin.site.register(IgnitionMethod, IgnitionMethodAdmin)
admin.site.register(AircraftType, AircraftTypeAdmin)
admin.site.register(AircraftRegistration, AircraftRegistrationAdmin)
admin.site.register(AviationRequest, AviationRequestAdmin)
