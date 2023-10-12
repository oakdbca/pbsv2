from django.db import models


class ReferenceNumberModel(models.Model):
    reference_number = models.CharField(
        max_length=9, null=True, blank=True, editable=False
    )

    class Meta:
        abstract = True

    def __str__(self):
        return (
            self.reference_number
            if self.reference_number
            else f"{self._MODEL_PREFIX()}{'?'*6}"
        )

    def _MODEL_PREFIX(self):
        if not hasattr(self, "MODEL_PREFIX"):
            raise NotImplementedError(
                f"{self.__class__.__name__} model has no `MODEL_PREFIX` attribute"
            )
        return self.MODEL_PREFIX

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.reference_number:
            new_lodgement_id = f"{self._MODEL_PREFIX()}{self.pk:06d}"
            self.reference_number = new_lodgement_id
            self.save()

    @property
    def model_name(self):
        return self._meta.model_name
