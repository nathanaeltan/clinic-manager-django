from rest_framework import viewsets
from procedure.serializers import ProcedureSerializer
from rest_framework.permissions import IsAuthenticated
from core.models import Procedure


class ProcedureViewSet(viewsets.ModelViewSet):
    serializer_class = ProcedureSerializer
    queryset = Procedure.objects.all()
    permission_classes = [IsAuthenticated]
