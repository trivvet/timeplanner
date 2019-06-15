from rest_framework.serializers import (
    ModelSerializer,
    SerializerMethodField
)

from ..models import Report, Judge, ReportEvents

class ReportListSerializer(ModelSerializer):
    class Meta:
        model = Report
        fields = (
            'id',
            'full_number',
            'number',
            'address',
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

class ReportDetailSerializer(ModelSerializer):
    judge_name = SerializerMethodField()
    events = SerializerMethodField()
    last_event = SerializerMethodField()
    class Meta:
        model = Report
        fields = (
            'id',
            'full_number',
            'case_number',
            'cost',
            'judge_name',
            'active',
            'executed',
            'active_days',
            'waiting_days',
            'events',
            'last_event'
        )

    def get_judge_name(self, obj):
        return JudgeDetailSerializer(obj.judge_name, many=False).data

    def get_events(self, obj):
        return ReportEventsSerializer(obj.events, many=True).data

    def get_last_event(self, obj):
        return ReportEventsSerializer(obj.last_event, many=False).data

class ReportEventsSerializer(ModelSerializer):
    class Meta:
        model = ReportEvents
        fields = (
            'date',
            'name',
            'subspecies'
        )

class JudgeDetailSerializer(ModelSerializer):
    class Meta:
        model = Judge
        fields = (
            'id',
            'description',
        )
