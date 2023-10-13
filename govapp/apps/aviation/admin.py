from django.contrib import admin

from .models import AircraftRegistration, AircraftType, AviationRequest, IgnitionMethod


class IgnitionMethodAdmin(admin.ModelAdmin):
    pass


class AircraftTypeAdmin(admin.ModelAdmin):
    pass


class AircraftRegistrationAdmin(admin.ModelAdmin):
    pass


class AviationRequestAdmin(admin.ModelAdmin):
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


admin.site.register(IgnitionMethod, IgnitionMethodAdmin)
admin.site.register(AircraftType, AircraftTypeAdmin)
admin.site.register(AircraftRegistration, AircraftRegistrationAdmin)
admin.site.register(AviationRequest, AviationRequestAdmin)
