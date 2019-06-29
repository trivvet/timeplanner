from django.contrib.auth import get_user_model

from rest_framework.serializers import (
    ModelSerializer,
    SerializerMethodField,
    CharField
)

from ..models import (
    Report, 
    Judge, 
    ReportEvents, 
    ReportParticipants,
    ReportSubject
    )

User = get_user_model()

class ReportListSerializer(ModelSerializer):
    last_event = SerializerMethodField()
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
            'waiting_days',
            'last_event'
        )

    def get_last_event(self, obj):
        return ReportEventsSerializer(obj.last_event, many=False).data

class ReportDetailSerializer(ModelSerializer):
    judge_name = SerializerMethodField()
    events = SerializerMethodField()
    last_event = SerializerMethodField()
    participants = SerializerMethodField()
    subjects = SerializerMethodField()
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
            'last_event',
            'participants',
            'subjects'
        )

    def get_judge_name(self, obj):
        return JudgeDetailSerializer(obj.judge_name, many=False).data

    def get_events(self, obj):
        return ReportEventsSerializer(obj.events, many=True).data

    def get_last_event(self, obj):
        return ReportEventsSerializer(obj.last_event, many=False).data

    def get_participants(self, obj):
        return ReportParticipantSerializer(
            obj.participants, many=True).data

    def get_subjects(self, obj):
        return ReportSubjectSerializer(
            obj.subjects, many=True).data

class ReportCreateAwardSerializer(ModelSerializer):
    class Meta:
        model = Report
        fields = ('number', 'number_year', 'plaintiff', 'defendant', 
            'address', 'object_name', 'research_kind', 'active')

class ReportEventsSerializer(ModelSerializer):
    class Meta:
        model = ReportEvents
        fields = (
            'date',
            'name',
            'subspecies',
            'short_info'
        )

class JudgeDetailSerializer(ModelSerializer):
    class Meta:
        model = Judge
        fields = (
            'id',
            'description',
        )

class ReportParticipantSerializer(ModelSerializer):
    class Meta:
        model = ReportParticipants
        fields = (
            'status',
            'full_name'
        )

class ReportSubjectSerializer(ModelSerializer):
    class Meta:
        model = ReportSubject
        fields = (
            'subject_type',
            'short_name'
        )


class AccountLoginSerializer(ModelSerializer):
    token = CharField(allow_blank=True, read_only=True)
    username = CharField(required=False, allow_blank=True, 
        label="Username")

    class Meta:
        model = User
        fields = (
            'username',
            'token'
        )
