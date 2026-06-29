from django.db import models
from apps.applications.models import JobApplication
from apps.users.models import User

# Create your models here.
class InterviewSchedule(models.Model):

    application = models.OneToOneField(
        JobApplication,
        on_delete=models.CASCADE
    )

    interview_date = models.DateField()

    interview_time = models.TimeField()

    status = models.CharField(
        max_length=20,
        default="scheduled"
    )

    created_at = models.DateTimeField(auto_now_add=True)


class AuditLog(models.Model):

    ACTIONS = (
        ("LOGIN", "LOGIN"),
        ("APPLICATION", "APPLICATION"),
        ("AI_INTERVIEW", "AI_INTERVIEW"),
        ("REPORT", "REPORT"),
        ("ADMIN", "ADMIN"),
    )

    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    action = models.CharField(
        max_length=30,
        choices=ACTIONS
    )

    description = models.TextField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.action