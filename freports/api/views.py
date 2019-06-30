from rest_framework.filters import OrderingFilter
from rest_framework.generics import (
    ListAPIView, 
    RetrieveAPIView,
    CreateAPIView,
    )
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from .serializers import (
    ReportListSerializer, 
    ReportDetailSerializer,
    ReportCreateAwardSerializer
    )
from ..models import Report

class ReportListApiView(ListAPIView):
    serializer_class = ReportListSerializer
    permission_classes = (IsAuthenticated,)
    queryset = Report.objects.all()
    filter_backends = (OrderingFilter,)
    ordering_fields = ('number', 'address')
    ordering = ('number',)

class ReportDetailApiView(RetrieveAPIView):
    serializer_class = ReportDetailSerializer
    permission_classes = (IsAuthenticated,)
    queryset = Report.objects.all()

class ReportCreateAwardApiView(CreateAPIView):
    queryset = Report.objects.all()
    serializer_class = ReportCreateAwardSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(
            plaintiff='-',
            defendant='-',
            address='-',
            object_name='-',
            research_kind='-',
            active=None
        )