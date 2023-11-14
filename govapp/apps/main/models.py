from abc import ABC, ABCMeta, abstractmethod
from typing import Any, Generic, TypeVar

from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models.fields.related_descriptors import ReverseManyToOneDescriptor
from protected_media.models import ProtectedFileField

model_type: Any = type(models.Model)
T = TypeVar("T")


class AbstractModelMeta(ABCMeta, model_type):
    pass


class YearField(models.IntegerField):
    def __init__(self, *args, **kwargs):
        kwargs["validators"] = [MinValueValidator(2023), MaxValueValidator(2100)]
        super().__init__(*args, **kwargs)


class GenericIntervalField(ABC, models.Field, Generic[T]):
    """A generic field class that accepts a min and max value (including both endpoints: `[min,max]`-notation)"""

    def __init__(
        self,
        *args,
        min_value=None,
        max_value=None,
        **kwargs: Any,
    ) -> None:
        if min_value is not None:
            kwargs["validators"] = kwargs.get("validators", []) + [
                MinValueValidator(min_value)
            ]
        if max_value is not None:
            kwargs["validators"] = kwargs.get("validators", []) + [
                MaxValueValidator(max_value)
            ]
        self.min_value, self.max_value = min_value, max_value

        self.field_class().__init__(self, *args, **kwargs)

    def formfield(self, **kwargs):
        defaults = {"min_value": self.min_value, "max_value": self.max_value}
        defaults.update(kwargs)
        return super().formfield(**defaults)

    @abstractmethod
    def field_class(self) -> type[T]:
        raise NotImplementedError("Must implement method field_class")


class IntervalIntegerField(
    models.IntegerField, GenericIntervalField[models.IntegerField]
):
    def field_class(self):
        return models.IntegerField


class UniqueNameableModel(models.Model):
    name = models.CharField(max_length=255, unique=True, null=False, blank=False)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class NameableModel(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class NullableNameableModel(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class DisplayNameableModel(models.Model):
    display_name = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.display_name


class ReferenceableModel(models.Model):
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


class AssignableModel(models.Model, metaclass=AbstractModelMeta):  # type: ignore
    assigned_to = models.ForeignKey(
        User, on_delete=models.PROTECT, null=True, blank=True
    )

    class Meta:
        abstract = True

    def assign(self, user: User):
        user_is_assignable, reason = self.user_is_assignable(user)
        if not user_is_assignable:
            raise ValueError(f"{user} is not assignable to {self} because {reason}")
        self.assigned_to = user
        self.save()

    def unassign(self):
        self.assigned_to = None
        self.save()

    @abstractmethod
    def user_is_assignable(self, user: User) -> tuple[bool, str]:
        """Models implementing this class must define a function
        that checks if a user is assignable to the model.

        Returns:
            A tuple of (bool, str) where the bool is True (and str is empty) if the user is assignable
            If the user is not assigned, the str is the reason why the user is not assignable.

        Args:
            user: The auth user model instance to check

        """
        return True, ""


class ArchivableModelManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(archived=False)

    def archived(self):
        return self.get_queryset().filter(archived=True)


class ArchivableModel(models.Model):
    objects = ArchivableModelManager()

    archived = models.BooleanField(default=False)

    class Meta:
        abstract = True

    def archive(self):
        self.archived = True
        self.save()

    def unarchive(self):
        self.archived = False
        self.save()


def file_upload_location(instance, filename):
    return f"uploads/{instance._meta.model_name}/{filename}"


class ModelFile(models.Model):
    file = ProtectedFileField(upload_to=file_upload_location)
    name = models.CharField(max_length=255, null=False, blank=False)
    description = models.TextField(null=True, blank=True)
    uploaded_by = models.ForeignKey(
        User, on_delete=models.PROTECT, null=True, blank=True
    )
    datetime_uploaded = models.DateTimeField(auto_now_add=True)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")

    class Meta:
        indexes = [
            models.Index(fields=["content_type", "object_id"]),
        ]

    def __str__(self):
        return self.name


class Region(DisplayNameableModel, UniqueNameableModel):
    class Meta:
        ordering = ["name"]

    def __str__(self):
        if not self.display_name:
            return self.name
        return self.display_name


class District(DisplayNameableModel, UniqueNameableModel):
    region = models.ForeignKey(
        Region, on_delete=models.CASCADE, null=False, blank=False
    )

    burnplanunitdistricts: ReverseManyToOneDescriptor

    burn_plan_units: models.Manager

    class Meta:
        ordering = ["region", "name"]

    def __str__(self):
        if not self.display_name:
            return self.name
        return self.display_name


class Lga(DisplayNameableModel, UniqueNameableModel):
    district = models.ForeignKey(
        District, on_delete=models.CASCADE, null=False, blank=False
    )

    operationalplanapprovals: ReverseManyToOneDescriptor

    class Meta:
        ordering = ["district", "name"]

    def __str__(self):
        if not self.display_name:
            return self.name
        return self.display_name
