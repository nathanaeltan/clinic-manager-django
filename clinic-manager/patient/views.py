from rest_framework import viewsets, status, generics
from patient.serializers import PatientSerializer, AppointmentSerializer, AppointmentCreateUpdateSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from core.models import Patient, Appointment


class PatientViewSet(viewsets.ModelViewSet):
    serializer_class = PatientSerializer
    queryset = Patient.objects.all()
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(
            self.get_queryset().filter(active=True)
            )
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.active = False
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class AppointmentViewSet(viewsets.ModelViewSet):
    queryset = Appointment.objects.all()
    permission_classes = [IsAuthenticated]
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['patient_pk'] = self.kwargs.get('patient_pk')  # Pass patient_pk from URL kwargs
        return context
    def get_serializer_class(self):
        if self.action in ['create']:
            return AppointmentCreateUpdateSerializer
        elif self.action in ['update', 'partial_update']:
            return AppointmentCreateUpdateSerializer
        return AppointmentSerializer



class ListAllAppointmentsView(generics.ListAPIView):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
