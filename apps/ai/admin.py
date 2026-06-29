from django.contrib import admin
from apps.ai.models import InterviewSchedule,AuditLog
# Register your models here.
admin.site.register(InterviewSchedule)
admin.site.register(AuditLog)
