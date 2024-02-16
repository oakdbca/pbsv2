# Third-Party
from django.contrib import auth
from django.contrib.auth.models import Group
from rest_framework import serializers

from govapp.apps.accounts.models import Profile

# Shortcuts
User = auth.get_user_model()


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = "__all__"


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


class ProfileSerializer(serializers.ModelSerializer):
    district = serializers.CharField(source="district.name_with_region")

    class Meta:
        model = Profile
        exclude = (
            "id",
            "user",
        )


class UserProfileSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()
    groups = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "profile",
            "groups",
        )

    def get_groups(self, obj):
        return obj.groups.values_list("name", flat=True)
