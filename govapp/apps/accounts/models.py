from django.contrib import auth
from django.db import models

from govapp.apps.main.models import District

User = auth.get_user_model()


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    district = models.ForeignKey(
        District, on_delete=models.CASCADE, null=True, blank=True
    )
