from rest_framework import serializers


class GenerateInterviewSerializer(serializers.Serializer):
    application_id = serializers.IntegerField()


class SubmitAnswerSerializer(serializers.Serializer):
    question_id = serializers.IntegerField()
    answer = serializers.CharField()


class InterviewResultSerializer(serializers.Serializer):
    session_id = serializers.IntegerField()

class ScheduleInterviewSerializer(serializers.Serializer):
    application_id = serializers.IntegerField()