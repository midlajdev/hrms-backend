# notifications/services.py
from celery import shared_task
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.conf import settings
from apps.notifications.models import EmailLog
from django.core.mail import EmailMessage

@shared_task
def send_notification(subject, template, context, email):
    try:
        message = render_to_string(template, context)

        email_message = EmailMessage(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [email],
        )
        email_message.content_subtype = "html"
        email_message.send()

        EmailLog.objects.create(
            email=email,
            subject=subject,
            status="SUCCESS"
        )

    except Exception as e:
        print(" EMAIL ERROR:", str(e))
        EmailLog.objects.create(
            email=email,
            subject=subject,
            status="FAILED",
            error=str(e)
        )

def notify_application_submitted(application):
    send_notification.delay(
        subject="Application Submitted",
        template="emails/application_submitted.html",
        context={
            "name": application.candidate.user.first_name,
            "job_title": application.job.title
        },
        email=application.candidate.user.email
    )
    
    print("EMAIL FUNCTION CALLED")
    print(application.candidate.user.email)


def notify_shortlisted(application):
    send_notification.delay(
        subject="You are shortlisted!",
        template="emails/shortlisted.html",
        context={
            "name": application.candidate.user.first_name,
            "job_title": application.job.title
        },
        email=application.candidate.user.email
    )


def notify_rejected(application):
    send_notification.delay(
        subject="Application Update",
        template="emails/rejected.html",
        context={
            "name": application.candidate.user.first_name,
            "job_title": application.job.title
        },
        email=application.candidate.user.email
    )

def notify_interview_scheduled(schedule):
    send_notification.delay(
        subject="AI Interview Scheduled",
        template="emails/interview_scheduled.html",
        context={
            "name": schedule.application.candidate.user.first_name,
            "job_title": schedule.application.job.title,
            "interview_date": schedule.interview_date,
            "interview_time": schedule.interview_time,
        },
        email=schedule.application.candidate.user.email
    )


# def notify_interview_reminder(schedule):
#     send_notification.delay(
#         subject="Interview Reminder",
#         template="emails/interview_reminder.html",
#         context={
#             "name": schedule.application.candidate.user.first_name,
#             "job_title": schedule.application.job.title,
#             "interview_date": schedule.interview_date,
#             "interview_time": schedule.interview_time,
#         },
#         email=schedule.application.candidate.user.email,
#     )


def notify_interview_reminder(schedule):

    email = schedule.application.candidate.user.email

    try:
        send_mail(
            subject="Interview Reminder",
            message=f"""
Interview Reminder

Job: {schedule.application.job.title}

Date: {schedule.interview_date}

Time: {schedule.interview_time}
""",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[email],
            fail_silently=False,
        )

        EmailLog.objects.create(
            email=email,
            subject="Interview Reminder",
            status="SUCCESS"
        )

    except Exception as e:

        EmailLog.objects.create(
            email=email,
            subject="Interview Reminder",
            status="FAILED",
            error=str(e)
        )

        raise