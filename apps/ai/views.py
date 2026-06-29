from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from apps.ai.serializers import GenerateInterviewSerializer
from apps.ai.services.interview_service import InterviewService
from apps.applications.models import JobApplication

from apps.ai.serializers import SubmitAnswerSerializer
from apps.ai.services.answer_service import AnswerService
from apps.applications.models import AIQuestion

from django.db.models import Avg
from apps.applications.models import AIInterviewSession, AIAnswer

from apps.ai.serializers import ScheduleInterviewSerializer
from apps.ai.services.schedule_service import ScheduleService
from apps.applications.models import JobApplication

from apps.ai.services.report_service import ReportService
from apps.users.permissions import IsEmployer
from apps.ai.services.analytics_service import AnalyticsService
from apps.jobs.models import Job
from apps.ai.services.logging_service import LoggingService
from apps.payments.permissions import HasActiveSubscription


class GenerateInterviewView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        try:

            serializer = GenerateInterviewSerializer(data=request.data)

            serializer.is_valid(raise_exception=True)

            application = JobApplication.objects.get(
                id=serializer.validated_data["application_id"]
            )

            service = InterviewService()

            session = service.generate_questions(
                application=application,
                triggered_by=request.user
            )

            LoggingService.log_action(
                request.user,
                "AI_INTERVIEW",
                f"Generated AI interview for application {application.id}"
            )

            return Response({
                "message": "Interview generated successfully.",
                "session_id": session.id,
                "questions_generated": session.questions.count(),
            })

        except Exception as e:

            return Response(
                {
                    "REAL_ERROR": str(e)
                },
                status=500
            )
    

class SubmitAnswerView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        serializer = SubmitAnswerSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        question_id = serializer.validated_data["question_id"]
        answer_text = serializer.validated_data["answer"]

        try:
            question = AIQuestion.objects.get(id=question_id)

        except AIQuestion.DoesNotExist:
            return Response(
                {"error": "Question not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        service = AnswerService()

        ai_answer = service.evaluate_answer(
            question,
            answer_text
        )

        return Response(
            {
                "message": "Answer evaluated successfully.",
                "score": ai_answer.confidence_score,
                "reason": ai_answer.transcript_json.get("reason")
            },
            status=status.HTTP_200_OK
        )
    
class InterviewResultView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, session_id):

        try:
            session = AIInterviewSession.objects.get(id=session_id)

        except AIInterviewSession.DoesNotExist:
            return Response(
                {"error": "Interview session not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        answers = AIAnswer.objects.filter(
            question__session=session
        )

        overall_score = answers.aggregate(
            Avg("confidence_score")
        )["confidence_score__avg"]

        return Response(
            {
                "session_id": session.id,
                "questions_answered": answers.count(),
                "overall_score": round(overall_score or 0, 2),
                "status": session.status,
            },
            status=status.HTTP_200_OK
        )
    

class ScheduleInterviewView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        serializer = ScheduleInterviewSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            application = JobApplication.objects.get(
                id=serializer.validated_data["application_id"]
            )

        except JobApplication.DoesNotExist:
            return Response(
                {"error": "Application not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        try:
            service = ScheduleService()
            schedule = service.schedule_interview(application)

            LoggingService.log_action(
                request.user,
                "APPLICATION",
                f"Scheduled AI interview for application {application.id}"
            )

        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        return Response(
            {
                "message": "Interview scheduled successfully.",
                "interview_date": schedule.interview_date,
                "interview_time": schedule.interview_time,
                "status": schedule.status,
            },
            status=status.HTTP_201_CREATED,
        )
    
class SendReminderView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        from apps.ai.services.reminder_service import send_interview_reminders

        try:
            count = send_interview_reminders()

            return Response({
                "message": f"{count} reminder(s) sent successfully."
            })

        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
class CandidateReportView(APIView):

    permission_classes = [
        IsAuthenticated,
        IsEmployer
    ]
    def get(self, request, session_id):
        try:
            session = AIInterviewSession.objects.get(
                id=session_id
            )
        except AIInterviewSession.DoesNotExist:
            return Response(
                {
                    "error": "Interview session not found"
                },
                status=status.HTTP_404_NOT_FOUND
            )
        try:
            report = ReportService().generate_report(session)
            LoggingService.log_action(
                request.user,
                "REPORT",
                f"Generated AI report for session {session.id}"
            )
            return Response(report)
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        


class RecruiterAnalyticsView(APIView):

    permission_classes = [
        IsAuthenticated,
        IsEmployer,
        HasActiveSubscription
    ]

    def get(self, request, job_id):

        try:

            job = Job.objects.get(
                id=job_id,
                employer__user=request.user
            )

        except Job.DoesNotExist:

            return Response(
                {
                    "error":"Job not found"
                },
                status=status.HTTP_404_NOT_FOUND
            )

        analytics = AnalyticsService().get_job_analytics(
            job
        )

        return Response(analytics)