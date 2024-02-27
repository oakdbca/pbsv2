from django.contrib import auth
from django.db import models
from django.utils.functional import cached_property

from govapp.apps.main.models import District

User = auth.get_user_model()


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    district = models.ForeignKey(
        District, on_delete=models.CASCADE, null=True, blank=True
    )

    @cached_property
    def cached_groups(self):
        return self.user.groups.all()
