from rest_framework.serializers import (
    ModelSerializer,
    SerializerMethodField
)

from ..models import Report, Judge

class ReportListSerializer(ModelSerializer):
    judge_name = SerializerMethodField()
    class Meta:
        model = Report
        fields = (
            'id',
            'full_number',
            'number',
            'case_number',
            'address',
            'cost',
            'judge_name',
            'plaintiff',
            'defendant',
            'object_name',
            'research_kind',
            'date_arrived',
            'date_executed',
            'active',
            'executed',
            'active_days',
            'waiting_days'
        )

    def get_judge_name(self, obj):
        return JudgeDetailSerializer(obj.judge_name, many=False).data

class ReportDetailSerializer(ModelSerializer):
    judge_name = SerializerMethodField()
    class Meta:
        model = Report
        fields = (
            'id',
            'full_number',
            'number',
            'case_number',
            'address',
            'cost',
            'judge_name',
            'plaintiff',
            'defendant',
            'object_name',
            'research_kind',
            'date_arrived',
            'active',
            'executed',
            'active_days',
            'waiting_days'
        )

    def get_judge_name(self, obj):
        return JudgeDetailSerializer(obj.judge_name, many=False).data

class JudgeDetailSerializer(ModelSerializer):
    class Meta:
        model = Judge
        fields = (
            'id',
            'description',
        )