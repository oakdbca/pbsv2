from django.contrib import admin

from govapp.apps.main.admin import NestedDeleteRestrictedAdmin

from .models import (
    BurnArea,
    FfdiRange,
    FuelType,
    GfdiRange,
    GlcRange,
    PmcRange,
    RhRange,
    RosRange,
    ScorchHeight,
    Sdi,
    SmcRange,
    TemperatureRange,
    WindDirection,
    WindSpeedRange,
)


@admin.register(FuelType)
class FuelTypeAdmin(NestedDeleteRestrictedAdmin):
    model = FuelType
    list_display = ("name",)


@admin.register(ScorchHeight)
class ScorchHeightAdmin(NestedDeleteRestrictedAdmin):
    model = ScorchHeight
    list_display = ("name",)


@admin.register(BurnArea)
class BurnAreaAdmin(NestedDeleteRestrictedAdmin):
    model = BurnArea
    list_display = ("name",)


@admin.register(RosRange)
class RosRangeAdmin(NestedDeleteRestrictedAdmin):
    model = RosRange
    list_display = ("name",)


@admin.register(FfdiRange)
class FfdiRangeAdmin(NestedDeleteRestrictedAdmin):
    model = FfdiRange
    list_display = ("name",)


@admin.register(GlcRange)
class GlcRangeAdmin(NestedDeleteRestrictedAdmin):
    model = GlcRange
    list_display = ("name",)


@admin.register(GfdiRange)
class GfdiRangeAdmin(NestedDeleteRestrictedAdmin):
    model = GfdiRange
    list_display = ("name",)


@admin.register(TemperatureRange)
class TemperatureRangeAdmin(NestedDeleteRestrictedAdmin):
    model = TemperatureRange
    list_display = ("name",)


@admin.register(RhRange)
class RhRangeAdmin(NestedDeleteRestrictedAdmin):
    model = RhRange
    list_display = ("name",)


@admin.register(Sdi)
class SdiAdmin(NestedDeleteRestrictedAdmin):
    model = Sdi
    list_display = ("name",)


@admin.register(SmcRange)
class SmcRangeAdmin(NestedDeleteRestrictedAdmin):
    model = SmcRange
    list_display = ("name",)


@admin.register(PmcRange)
class PmcRangeAdmin(NestedDeleteRestrictedAdmin):
    model = PmcRange
    list_display = ("name",)


@admin.register(WindSpeedRange)
class WindSpeedRangeAdmin(NestedDeleteRestrictedAdmin):
    model = WindSpeedRange
    list_display = ("name",)


@admin.register(WindDirection)
class WindDirectionAdmin(NestedDeleteRestrictedAdmin):
    model = WindDirection
    list_display = ("name",)
