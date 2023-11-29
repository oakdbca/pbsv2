from govapp.apps.main.models import UniqueNameableModel


class FuelType(UniqueNameableModel):
    class Meta:
        verbose_name = "Fuel Type"
        verbose_name_plural = "Fuel Types"
