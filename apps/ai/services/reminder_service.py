from django.utils import timezone
from datetime import timedelta

from apps.ai.models import InterviewSchedule
from services.notification_email import notify_interview_reminder


def send_interview_reminders():

    tomorrow = timezone.now().date() + timedelta(days=1)

    interviews = InterviewSchedule.objects.filter(
        interview_date=tomorrow,
        status="scheduled"
    )

    for interview in interviews:
        notify_interview_reminder(interview)

    return interviews.count()