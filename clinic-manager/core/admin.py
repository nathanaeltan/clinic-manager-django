from django.contrib import admin
from core.models import User, Patient, Medication, PatientMedication, Procedure, Appointment

# Register your models here.

admin.site.register(User)
admin.site.register(Patient)
admin.site.register(Medication)
admin.site.register(PatientMedication)
admin.site.register(Procedure)
admin.site.register(Appointment)
