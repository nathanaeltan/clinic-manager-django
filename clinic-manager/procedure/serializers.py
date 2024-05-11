from rest_framework import serializers
from core.models import Procedure


class ProcedureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Procedure
        fields = ["id", "name", "description"]

class CreateAppointmentProcedureSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(queryset=Procedure.objects.all(), required=True)

    class Meta:
        model = Procedure
        fields = ["id"]



