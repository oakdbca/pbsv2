import logging
from typing import Any, Optional

from wagov_utils.components.utils.email import (
    TemplateEmailBase as WAGovUtilsTemplateEmailBase,
)

# Logging
log = logging.getLogger(__name__)


class TemplateEmailBase(WAGovUtilsTemplateEmailBase):
    def send_to(
        self,
        *users: Any,
        context: Optional[dict[str, Any]] = None,
    ) -> None:
        """Sends an email individually to many users.

        Args:
            *users (Any): Possible users to send the email to.
            context (Optional[dict[str, Any]]): Context for the template.
        """
        # Filter the supplied users to only objects that have an `email`
        # attribute, and cast them to a set to eliminate any duplicated

        for user in users:
            if not hasattr(user, "email"):
                continue
            context = context if context else {}
            context["first_name"] = (
                user.first_name if hasattr(user, "first_name") else user.name
            )
            self.send(user.email, context=context)
