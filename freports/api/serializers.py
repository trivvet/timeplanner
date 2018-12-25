from rest_framework.serializers import ModelSerializer

from ..models import Report

class ReportListSerializer(ModelSerializer):
    class Meta:
        model = Report
        fields = (
            'number',
            'number_year',
            'address',
            'judge_name',
            'plaintiff',
            'defendant',
            'object_name',
            'research_kind',
        )