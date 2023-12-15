from abc import abstractmethod

from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models
from model_utils import Choices
from model_utils.models import TimeStampedModel

from govapp.apps.main.models import (
    AbstractModelMeta,
    DisplayNameableModel,
    Lga,
    LodgementDateModel,
    ModelFile,
    UniqueNameableModel,
)


# Let's call the class LegalApproval to not confuse with an Approval model
class LegalApproval(UniqueNameableModel, DisplayNameableModel):
    """Burn Program and Operational Area/Operational Plan approvals"""

    objects = models.Manager()

    modellegalapprovals: "models.Manager[ModelLegalApproval]"

    # TODO Not sure on this one, but requirement item #72 mentions these three separately
    APPROVAL_TYPES = Choices(
        ("endorsement", "Endorsement"),
        ("approval", "Approval"),
        ("endorsement_or_approval", "Endorsement/Approval"),
    )
    approval_type = models.CharField(
        max_length=255, choices=APPROVAL_TYPES, null=True, blank=True
    )
    # TODO There must be a better term than land_type?
    LAND_TYPE_SHIRE = "shire"
    LAND_TYPES = Choices(
        (LAND_TYPE_SHIRE, "Shire"),
        ("owner", "Owner"),
        ("other", "Other Lands"),
    )
    land_type = models.CharField(
        max_length=255, choices=LAND_TYPES, null=True, blank=True
    )  # To be added by the system after intersection

    approver: models.CharField = models.CharField(
        max_length=255, null=True, blank=True
    )  # Corporate Executive, Shire, Other Lands, Owner

    has_additional_permissions: models.BooleanField = models.BooleanField(
        default=False
    )  # Whether the user can attach files, texts, or remove the approval
    is_required_for_operational_area = models.BooleanField(default=False)
    is_required_for_operational_plan = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Legal/Approval"
        verbose_name_plural = "Legal/Approvals"

    def __str__(self) -> str:
        return f"{self.approver} {self.get_approval_type_display()}"

    @property
    def is_shire_approval(self):
        return self.land_type == self.LAND_TYPE_SHIRE

    @property
    def can_remove_approval(self):
        return self.has_additional_permissions and self.text_remove_justification


class OtherApproval(
    LodgementDateModel,
):
    reference_number = models.CharField(
        max_length=9, null=True, blank=True, editable=True
    )  # The reference number of the other approval (DAS or ATT)

    def __str__(self) -> str:
        if not self.reference_number:
            return f"Other Approval ({self.lodgement_date})"

        self.related_issuance
        return (
            f"{self.related_issuance}: {self.reference_number} ({self.lodgement_date})"
        )

    @property
    def related_issuance(self):
        """Returns the related issuance type (DAS or ATT or possibly something new added in the future)"""

        related_issuance_fields = [
            attr
            for attr in dir(self)
            if attr.endswith("_proposals") or attr.endswith("_approvals")
        ]
        # Classnames could potentially contain an underscore, so we need to join all but the last part
        related_classnames = list(
            {"_".join(x.split("_")[:-1]) for x in related_issuance_fields}
        )
        qs = OtherApproval.objects.none()
        for classname in related_classnames:
            has_proposals = getattr(self, f"{classname}_proposals", qs).all().exists()
            has_approvals = getattr(self, f"{classname}_approvals", qs).all().exists()
            if not has_proposals and not has_approvals:
                continue

            qs = (
                getattr(self, f"{classname}_proposals", qs)
                if has_proposals
                else getattr(self, f"{classname}_approvals", qs)
            )
            if qs.exists():
                return qs.all().first().__class__.__name__

        return "None"


class DisturbanceApplication(models.Model):
    proposal = models.ForeignKey(
        OtherApproval,
        on_delete=models.CASCADE,
        related_name="%(class)s_proposals",
    )
    approval = models.ForeignKey(
        OtherApproval,
        on_delete=models.CASCADE,
        related_name="%(class)s_approvals",
    )

    class Meta:
        verbose_name = "Disturbance Application"
        verbose_name_plural = "Disturbance Applications"

    def __str__(self) -> str:
        return f"Proposal: {self.proposal} - Approval: {self.approval}"


class AuthorityToTake(models.Model):
    application = models.ForeignKey(
        OtherApproval,
        on_delete=models.CASCADE,
        related_name="%(class)s_proposals",
    )  # Calling the related name `proposals`` so this class can be inferred from OtherApproval
    issuance = models.ForeignKey(
        OtherApproval,
        on_delete=models.CASCADE,
        related_name="%(class)s_approvals",
    )  # Calling the related name `approvals`` so this class can be inferred from OtherApproval

    class Meta:
        verbose_name = "Authority to Take"
        verbose_name_plural = "Authorities to Take"

    def __str__(self) -> str:
        return f"Application: {self.application} - Issuance: {self.issuance}"


class ModelLegalApproval(TimeStampedModel):
    file_as_approval = GenericRelation(ModelFile)
    text_as_approval: models.TextField = models.TextField(null=True, blank=True)
    text_remove_justification: models.TextField = models.TextField(
        null=True, blank=True
    )

    legal_approval = models.ForeignKey(
        LegalApproval,
        on_delete=models.CASCADE,
        related_name="modellegalapprovals",
    )  # OP: endorsement and approval by district manager and regional manager

    lga: models.ForeignKey = models.ForeignKey(
        Lga,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        verbose_name="Shire/LGA",
        related_name="modellegalapprovals",
    )  # Shire

    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        related_name="content_type_legal_approval",
    )
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")

    class Meta:
        verbose_name_plural = "Legal/Approvals"
        indexes = [
            models.Index(fields=["content_type", "object_id"]),
        ]

    def __str__(self) -> str:
        return (
            f"{self.legal_approval} entry for "
            f"{self.content_object.__class__.__name__} {self.content_object.__str__()} "
        )

    @property
    def has_lga(self):
        if not hasattr(self, "legal_approval"):
            raise AttributeError(
                "Model needs to implement a foreign key to LegalApproval to access `has_lga`"
            )
        return self.legal_approval.has_lga

    @property
    def has_additional_permissions(self):
        if not hasattr(self, "legal_approval"):
            raise AttributeError(
                "Model needs to implement a foreign key to LegalApproval to access `has_additional_permissions`"
            )
        return self.legal_approval.has_additional_permissions

    def clean(self) -> None:
        return super().clean()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)


class ModelRequiredApproval(DisplayNameableModel):
    legal_approval_name = models.CharField(max_length=255)
    is_required = models.BooleanField(default=False)

    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        related_name="content_type_required_approval",
    )
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")

    class Meta:
        unique_together = (
            "legal_approval_name",
            "content_type",
            "object_id",
        )
        verbose_name_plural = "Required Approvals"
        indexes = [
            models.Index(fields=["content_type", "object_id"]),
        ]

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.display_name:
            try:
                legal_approval = LegalApproval.objects.get(
                    name=self.legal_approval_name
                )
            except LegalApproval.DoesNotExist:
                raise ValueError(
                    f"LegalApproval with name {self.legal_approval_name} does not exist"
                )
            else:
                self.display_name = legal_approval.approver
                self.save()

    def __str__(self) -> str:
        required = "required" if self.is_required else "not required"
        return (
            f"{self.display_name} Endorsement/Approval is {required} for "
            f"{self.content_object.__class__.__name__} {self.content_object.__str__()}"
        )


class ApprovableModel(models.Model, metaclass=AbstractModelMeta):
    required_approvals = GenericRelation(ModelRequiredApproval)
    legal_approvals = GenericRelation(ModelLegalApproval)

    # OP: lodgement dates of DAS proposal + approval and expiry date of the issued DAS approvals
    disturbance_application: models.ManyToManyField = models.ManyToManyField(
        DisturbanceApplication,
        related_name="%(class)s_das_approvals",
    )
    # OP: lodgement date of the related Flora and Fauna 'Authority To Take' lawful authorities
    # + issue and expiry date of the issued lawful authorities
    flora_authority_to_take = models.ForeignKey(
        AuthorityToTake,
        on_delete=models.CASCADE,
        related_name="%(class)s_flora_atts",
        null=True,
        blank=True,
    )
    fauna_authority_to_take = models.ForeignKey(
        AuthorityToTake,
        on_delete=models.CASCADE,
        related_name="%(class)s_fauna_atts",
        null=True,
        blank=True,
    )

    class Meta:
        abstract = True

    def clean(self):
        return super().clean()

    def save(self, *args, **kwargs):
        is_new_object = self.pk is None
        super().save(*args, **kwargs)

        if is_new_object:
            # Automatically create required approval entries for the model
            for name in self.initial_required_approvals():
                ModelRequiredApproval.objects.create(
                    content_object=self,
                    legal_approval_name=name,
                    is_required=True,
                )
            for name in self.initial_not_required_approvals():
                ModelRequiredApproval.objects.create(
                    content_object=self,
                    legal_approval_name=name,
                    is_required=False,
                )

    @abstractmethod
    def initial_required_approvals(self):
        """Needs to be implemented by the model to return a list of LegalApproval names
        that are required
        """

        return LegalApproval.objects.none()

    @abstractmethod
    def initial_not_required_approvals(self):
        """Needs to be implemented by the model to return a list of LegalApproval names
        that are not required
        """

        return LegalApproval.objects.none()
