from django.contrib import admin
from .models import JobApplication, ApplicationStatusLog, AIInterviewSession, AIQuestion, AIAnswer, CallLog
# Register your models here.
@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):
    list_display = ("id","candidate","job","resume_snapshot","status","applied_date")

@admin.register(ApplicationStatusLog)
class ApplicationStatusLogAdmin(admin.ModelAdmin):
    list_display = ("application", "old_status", "new_status", "changed_by", "changed_at")

@admin.register(AIInterviewSession)
class AIInterviewSessionAdmin(admin.ModelAdmin):
    list_display = ("id","candidate")

@admin.register(AIQuestion)
class AIQuestionAdmin(admin.ModelAdmin):
    list_display = ("id","question_text","session")
admin.site.register(AIAnswer)
admin.site.register(CallLog)