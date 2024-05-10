from rest_framework import serializers
from core.models import Patient, PatientMedication, Medication


class MedicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medication
        fields = ["id", "name"]


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
