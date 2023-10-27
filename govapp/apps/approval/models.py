from logging import getLogger

from django.db import models
from model_utils import Choices
from model_utils.models import TimeStampedModel
from protected_media.models import ProtectedFileField

from govapp.apps.main.models import Lga, file_upload_location

logger = getLogger(__name__)


class Approval(TimeStampedModel):
    """Burn Program and Operational Area approvals"""

    # TODO What is the difference between an approval and an endorsement?
    APPROVAL_TYPE = Choices(
        ("approval", "Approval"),
        ("endorsement", "Endorsement"),
    )
    approver: models.CharField = models.CharField(
        max_length=255, null=True, blank=True
    )  # Corporate Executive, Shire, Other Lands, Owner
    lga: models.ForeignKey = models.ForeignKey(
        Lga, on_delete=models.PROTECT, null=True, blank=True
    )  # Shire

    can_provide_evidence: models.BooleanField = models.BooleanField(
        default=False
    )  # Whether the user can attach files, texts, or remove the approval
    file_as_approval = ProtectedFileField(upload_to=file_upload_location)
    text_as_approval: models.TextField = models.TextField(null=True, blank=True)
    text_remove_justification: models.TextField = models.TextField(
        null=True, blank=True
    )

    def __str__(self):
        if self.lga:
            return f"{self.approver} {self.APPROVAL_TYPE} {self.lga}"
        return f"{self.approver} {self.APPROVAL_TYPE}"
