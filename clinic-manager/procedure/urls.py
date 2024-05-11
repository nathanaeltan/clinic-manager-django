from django.urls import (
    path,
    include,
)

from rest_framework.routers import DefaultRouter
from procedure import views

router = DefaultRouter()
router.register("", views.ProcedureViewSet)
app_name = "procedure"

urlpatterns = [path("", include(router.urls))]
