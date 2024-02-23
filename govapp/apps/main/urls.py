from django import urls
from rest_framework import routers

from govapp.apps.main import views

router = routers.DefaultRouter()

router.register(r"regions", views.RegionViewSet, basename="regions")
router.register(r"districts", views.DistrictViewSet, basename="districts")

urlpatterns = [
    urls.path("api/", urls.include(router.urls)),
]
