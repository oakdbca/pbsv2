from django.contrib.auth.models import User
from django.db import models

from govapp.apps.main.models import District


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    district = models.ForeignKey(
        District, on_delete=models.CASCADE, null=True, blank=True
    )
