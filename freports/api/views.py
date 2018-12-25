from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

from .serializers import ReportListSerializer
from ..models import Report

class ReportListApiView(ListAPIView):
    serializer_class = ReportListSerializer
    ordering_fields = ('number',)
    permission_classes = (IsAuthenticated,)
    queryset = Report.objects.all()