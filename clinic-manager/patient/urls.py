from django.urls import (
    path,
    include,
)

from rest_framework.routers import DefaultRouter
from patient import views

router = DefaultRouter()
router.register("", views.PatientViewSet)
app_name = "patient"

urlpatterns = [path("", include(router.urls))]