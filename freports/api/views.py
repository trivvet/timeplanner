from rest_framework.filters import OrderingFilter
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

from .serializers import ReportListSerializer
from ..models import Report

class ReportListApiView(ListAPIView):
    serializer_class = ReportListSerializer

    permission_classes = (IsAuthenticated,)
    queryset = Report.objects.all()
    filter_backends = (OrderingFilter,)
    ordering_fields = ('number', 'address')
    ordering = ('number',)