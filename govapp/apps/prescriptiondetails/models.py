from govapp.apps.main.models import UniqueNameableModel


class FuelType(UniqueNameableModel):
    class Meta:
        verbose_name = "Fuel Type"
        verbose_name_plural = "Fuel Types"


class ScorchHeight(UniqueNameableModel):
    class Meta:
        verbose_name = "Scorch Height"
        verbose_name_plural = "Scorch Heights"


class BurnArea(UniqueNameableModel):
    class Meta:
        verbose_name = "Area to be burnt"
        verbose_name_plural = "Areas to be burnt"


class RosRange(UniqueNameableModel):
    class Meta:
        verbose_name = "Rate of Spread (ROS)"
        verbose_name_plural = "Rates of Spread (ROS)"


class FfdiRange(UniqueNameableModel):
    class Meta:
        verbose_name = "Forest Fire Danger Index (FFDI)"
        verbose_name_plural = "Forest Fire Danger Indices (FFDI)"


class GlcRange(UniqueNameableModel):
    class Meta:
        verbose_name = "Ground Level Concentration??? (GLC)"
        verbose_name_plural = "Ground Level Concentrations??? (GLC)"


class GfdiRange(UniqueNameableModel):
    class Meta:
        verbose_name = "Grass Fire Danger Index (GFDI)"
        verbose_name_plural = "Grass Fire Danger Indices (GFDI)"


class TemperatureRange(UniqueNameableModel):
    class Meta:
        verbose_name = "Temperature"
        verbose_name_plural = "Temperatures"


class RhRange(UniqueNameableModel):
    class Meta:
        verbose_name = "Relative Humidity (RH)"
        verbose_name_plural = "Relative Humidities (RH)"


class Sdi(UniqueNameableModel):
    class Meta:
        verbose_name = "Soil Dryness Index (SDI)"
        verbose_name_plural = "Soil Dryness Index (SDI)"


class SmcRange(UniqueNameableModel):
    class Meta:
        verbose_name = "Surface Fuel Moisture Content (SMC)"
        verbose_name_plural = "Surface Fuel Moisture Contents (SMC)"


class PmcRange(UniqueNameableModel):
    class Meta:
        verbose_name = "Profile Fuel Moisture Content (PMC)"
        verbose_name_plural = "Profile Fuel Moisture Contents (PMC)"


class WindSpeedRange(UniqueNameableModel):
    class Meta:
        verbose_name = "Wind Speed"
        verbose_name_plural = "Wind Speeds"


class WindDirection(UniqueNameableModel):
    class Meta:
        verbose_name = "Wind Direction"
        verbose_name_plural = "Wind Directions"
