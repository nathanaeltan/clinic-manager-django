from rest_framework import viewsets
from medication.serializers import MedicationSerializer
from rest_framework.permissions import IsAuthenticated
from core.models import Medication

class MedicationViewSet(viewsets.ModelViewSet):
    serializer_class = MedicationSerializer
    queryset = Medication.objects.all()
    permission_classes = [IsAuthenticated]
