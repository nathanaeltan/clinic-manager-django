from django.contrib import admin
from core.models import User, Patient, Medication, PatientMedication

# Register your models here.

admin.site.register(User)
admin.site.register(Patient)
admin.site.register(Medication)
admin.site.register(PatientMedication)
