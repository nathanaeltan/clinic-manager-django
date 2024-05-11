from rest_framework import serializers
from core.models import (
    Patient,
    PatientMedication,
    Medication,
    Appointment,
    Procedure,
)
from medication.serializers import MedicationSerializer
from procedure.serializers import (
    ProcedureSerializer,

)


class PatientMedicationSerializer(serializers.ModelSerializer):
    medication = MedicationSerializer()

    class Meta:
        model = PatientMedication
        fields = ["medication", "dosage", "frequency", "start_date", "end_date"]


class PatientSerializer(serializers.ModelSerializer):

    medications = PatientMedicationSerializer(
        many=True, required=False, source="patientmedication_set"
    )

    class Meta:
        model = Patient
        fields = [
            "id",
            "first_name",
            "last_name",
            "id_number",
            "gender",
            "height",
            "weight",
            "created_at",
            "updated_at",
            "active",
            "medications",
        ]
        read_only_fields = ["id", "active", "created_at", "updated_at"]

    def get_name(self):
        return f"{self.first_name} {self.last_name}"

    def _process_medication_data(self, patient, medication_data):
        medication = medication_data.pop("medication", None)
        medication_instance = Medication.objects.filter(**medication).first()
        if medication_instance:
            PatientMedication.objects.create(
                patient=patient, medication=medication_instance, **medication_data
            )

    def create(self, validated_data):
        medications_data = validated_data.pop("patientmedication_set", [])
        patient = Patient.objects.create(**validated_data)
        if medications_data:
            for medication_data in medications_data:
                self._process_medication_data(patient, medication_data)
        return patient

    def update(self, instance, validated_data):
        medications_data = validated_data.pop("patientmedication_set", [])
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if medications_data is not None:
            for patient_medication in instance.patientmedication_set.all():
                patient_medication.delete()

            for medication_data in medications_data:
                self._process_medication_data(instance, medication_data)
        instance.save()

        return instance


class PatientAppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = ["id", "first_name", "last_name"]


class ProcedureAppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Procedure
        fields = ["id", "name"]

class DynamicFieldsCategorySerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        # Don't pass the 'fields' arg up to the superclass
        fields = kwargs.pop('fields', None)

        # Instantiate the superclass normally
        super().__init__(*args, **kwargs)

        if fields is not None:
            # Drop any fields that are not specified in the `fields` argument.
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)

class AppointmentCreateUpdateSerializer(DynamicFieldsCategorySerializer):
    # procedures = ProcedureAppointmentSerializer(many=True)

    class Meta:
        model = Appointment
        fields = ["procedures", "start_time", "end_time"]

    def create(self, validated_data):
        patient_pk = self.context.get('patient_pk')
        try:
            patient = Patient.objects.get(pk=patient_pk)
        except Patient.DoesNotExist:
            raise serializers.ValidationError("Patient not found")

        validated_data['patient'] = patient
        procedures_data = validated_data.pop('procedures', [])
        appointment = Appointment.objects.create(**validated_data)

        appointment.procedures.set(procedures_data)
        return appointment


class AppointmentSerializer(serializers.ModelSerializer):
    patient = PatientAppointmentSerializer()
    procedures = ProcedureAppointmentSerializer(many=True)

    class Meta:
        model = Appointment
        fields = "__all__"


