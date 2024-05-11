# from django.urls import path, include
# from rest_framework.routers import DefaultRouter
# from rest_framework_nested import routers
# from patient import views

# router = routers.DefaultRouter()
# router.register("", views.PatientViewSet)
# appointment_router = routers.NestedSimpleRouter(router, r'patients', lookup='patient')
# appointment_router.register(r'appointments', views.AppointmentViewSet, basename='patient-appointments')




# app_name = "patient"

# urlpatterns = [
#     path("", include(router.urls)),
#     path('', include(appointment_router.urls)),
#     # path("<int:patient_id>/appointment/", views.AppointmentViewSet.as_view({"get": "list", "post":"create"}), name="patient-appointments"),
#     # path("<int:patient_id>/appointment/<int:pk>/", views.AppointmentViewSet.as_view({"get": "retrieve", "put": "update",}), name="appointment-detail"),
# ]
from django.urls import path, include
from rest_framework_nested import routers
from patient import views
router = routers.DefaultRouter()
router.register("", views.PatientViewSet)
appointment_router = routers.NestedSimpleRouter(router, r'', lookup='patient')
appointment_router.register(r'appointment', views.AppointmentViewSet, basename='patient-appointments')

app_name = "patient"

urlpatterns = [
    path("all-appointments/", views.ListAllAppointmentsView.as_view(), name="all-appointments"),
    path("", include(router.urls)),
    path("", include(appointment_router.urls)),
    # Other URL patterns for patient app if any
]