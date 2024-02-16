# Third-Party
from django.contrib import auth
from django.contrib.auth.models import Group
from rest_framework import serializers

from govapp.apps.accounts.models import Profile

# Shortcuts
User = auth.get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "groups",
            "first_name",
            "last_name",
            "email",
            "is_active",
            "is_staff",
        )


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ("id", "name", "permissions")


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = "__all__"


class UserProfileSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()

    class Meta:
        model = User
        exclude = ("password", "is_superuser", "is_staff", "is_active")
