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
    ReportCreateAwardSerializer,
    AccountLoginSerializer
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

class AccountLoginAPIView(APIView):
    serializer_class = AccountLoginSerializer

    def get(self, request, format=None):
        console.log("lkdja;lgkjdal;")
        # token = Token.objects.create(user=request.user)
        content = {
            'user': unicode(request.user),  # `django.contrib.auth.User` instance.
            'auth': unicode(request.auth),  # None
            # 'token': unicode(token)
        }
        return Response(content)

    # def post(self, request, *args, **kwargs):
    #     data = request.POST
    #     serializer = self.serializer_class(data=data)
    #     # import pdb;pdb.set_trace()
    #     if serializer.is_valid(raise_exception=True):
    #         new_data = serializer.data
    #         # user = serializer.validated_data['username']
    #         # token, created = Token.objects.get(user=user)
    #         return Response(new_data, status=HTTP_200_OK)
    #     else:
    #         return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)