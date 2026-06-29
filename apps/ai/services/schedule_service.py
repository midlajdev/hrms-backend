from datetime import timedelta, time
from services.notification_email import notify_interview_scheduled
from django.utils import timezone

from apps.ai.models import InterviewSchedule


class ScheduleService:
    """
    Simple interview scheduling engine.
    """

    def schedule_interview(self, application):

        # Check if already scheduled
        existing_schedule = InterviewSchedule.objects.filter(
            application=application
        ).first()

        if existing_schedule:
            return existing_schedule
        # Schedule for tomorrow at 10:00 AM
        interview_date = timezone.now().date() + timedelta(days=1)
        interview_time = time(10, 0)

        # Simple conflict resolution
        while InterviewSchedule.objects.filter(
            interview_date=interview_date,
            interview_time=interview_time
        ).exists():

            interview_time = time(interview_time.hour + 1, 0)

            if interview_time.hour > 17:
                interview_date += timedelta(days=1)
                interview_time = time(10, 0)

        schedule = InterviewSchedule.objects.create(
            application=application,
            interview_date=interview_date,
            interview_time=interview_time,
            status="scheduled"
        )

        notify_interview_scheduled(schedule)


        return schedule