from django.urls import (
    path,
    include,
)

from rest_framework.routers import DefaultRouter
from medication import views

router = DefaultRouter()
router.register("", views.MedicationViewSet)
app_name = "medication"

urlpatterns = [path("", include(router.urls))]
