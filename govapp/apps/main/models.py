from abc import ABC, ABCMeta, abstractmethod
from typing import Any, Generic, TypeVar

from django import forms
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models.fields.related_descriptors import ReverseManyToOneDescriptor
from django.utils.text import slugify
from protected_media.models import ProtectedFileField

model_type = models.base.ModelBase
T = TypeVar("T")


class AbstractModelMeta(ABCMeta, model_type):
    pass


class DetailMeta(AbstractModelMeta):
    """A metaclass that allows to define a model's verbose name and plural name"""

    def __new__(cls, name, bases, attrs, **kwargs):
        result = super().__new__(cls, name, bases, attrs, **kwargs)
        details = cls._DETAILS(result)

        if "detail_key" in attrs:
            if not attrs["detail_key"] in details:
                raise NotImplementedError(
                    "Model class must have a key that is in PRESCRIPTION_DETAILS"
                )
            verbose_name = details[attrs["detail_key"]].get("singular", None)
            verbose_name_plural = details[attrs["detail_key"]].get("plural", None)
            abbreviation = details[attrs["detail_key"]].get("abbreviation", None)
            abbreviation = (
                f" ({abbreviation})" if abbreviation or len(abbreviation) else ""
            )
            _meta = {
                "verbose_name": f"{verbose_name}{abbreviation}",
                "verbose_name_plural": f"{verbose_name_plural}{abbreviation}",
            }
            result._meta.__dict__.update(_meta)

        return result

    def _DETAILS(self):
        if not hasattr(self, "DETAILS"):
            raise NotImplementedError(
                f"{self.__class__.__name__} model has no `DETAILS` attribute"
            )
        return self.DETAILS


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


class YearField(IntervalIntegerField):
    def __init__(self, *args, **kwargs):
        super().__init__(min_value=2023, max_value=2100, *args, **kwargs)


class IntervalFloatField(models.FloatField, GenericIntervalField[models.FloatField]):
    def field_class(self):
        return models.FloatField


class RichTextEditorWidget(forms.Textarea):
    """Overwrite Textarea form to not be so obnoxiously large, so it can be used in i.e. tabular inlines."""

    def __init__(self, *args, **kwargs):
        cols = kwargs.pop("cols", 40)
        rows = kwargs.pop("rows", 10)

        attrs = kwargs.setdefault("attrs", {})
        attrs.setdefault("cols", cols)
        attrs.setdefault("rows", rows)

        super().__init__(*args, **kwargs)


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
        if not self.display_name:
            # If the display name is not set, return something that is not None
            return "Unknown"
        return self.display_name

    def save(self, *args, **kwargs):
        if not self.display_name and hasattr(self, "name") and self.name:
            self.display_name = self.name
        super().save(*args, **kwargs)


class OrdinalScaleModel(NameableModel):
    """A model that allows to associate a scalable value with a qualitative name"""

    ordinal_scale = models.PositiveSmallIntegerField(default=0, null=True, blank=True)

    class Meta:
        abstract = True
        unique_together = ("name", "ordinal_scale")

    def __str__(self):
        return f"{self.name} ({self.ordinal_scale})"


class LodgementDateModel(models.Model):
    lodgement_date = models.DateField(null=True, blank=True)
    issue_date = models.DateField(null=True, blank=True)
    approval_date = models.DateField(null=True, blank=True)
    expiry_date = models.DateField(null=True, blank=True)

    class Meta:
        abstract = True


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


class AssignableModel(models.Model, metaclass=AbstractModelMeta):
    assigned_to = models.ForeignKey(
        User, on_delete=models.PROTECT, null=True, blank=True
    )

    class Meta:
        abstract = True

    def assign(self, user: User):
        if not self.user_is_assignable(user):
            raise ValueError(f"{user} is not assignable to {self}")
        self.assigned_to = user
        self.save()

    def unassign(self):
        self.assigned_to = None
        self.save()

    def user_is_assignable(self, user: User) -> bool:
        return self.assignable_users().filter(pk=user.pk, is_active=True).exists()

    @abstractmethod
    def assignable_users(self) -> models.QuerySet[User]:
        """Models implementing this class must define
        a function that returns a queryset of users that are assignable to the model."""

        raise NotImplementedError("Must implement method assignable_users")


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
    content_type_name = slugify(instance.content_type.name)
    return f"uploads/{content_type_name}/{instance.object_id}/files/{filename}"


class DocumentCategory(UniqueNameableModel):
    pass


class DocumentDescriptor(UniqueNameableModel):
    pass


class ModelFile(models.Model):
    file = ProtectedFileField(upload_to=file_upload_location)
    name = models.CharField(max_length=255, null=False, blank=False)
    category = models.ForeignKey(
        DocumentCategory, on_delete=models.PROTECT, null=True, blank=True
    )
    descriptor = models.ForeignKey(
        DocumentDescriptor, on_delete=models.PROTECT, null=True, blank=True
    )
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

    @property
    def name_with_region(self):
        return f"{self.name} ({self.region})"


class Lga(DisplayNameableModel, UniqueNameableModel):
    operationalplanapprovals: ReverseManyToOneDescriptor
    operationalareaapprovals: ReverseManyToOneDescriptor
    modellegalapprovals: ReverseManyToOneDescriptor

    class Meta:
        ordering = ["name"]

    def __str__(self):
        if not self.display_name:
            return self.name
        return self.display_name


class NeighbourRole(UniqueNameableModel):
    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Neighbour(DisplayNameableModel, NameableModel):
    phone = models.CharField(max_length=255, null=True, blank=True)
    # Assuming the Interest field from the screenshot is equivalent to the Role field mentioned in the reqs
    role = models.ForeignKey(
        NeighbourRole, on_delete=models.PROTECT, null=True, blank=True
    )
    location = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        if not self.display_name:
            return self.name
        return f"{self.name} ({self.location})"
