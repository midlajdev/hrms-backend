from django.contrib import admin
from apps.jobs.models import Job, SavedJob
# Register your models here.
@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ("id","employer","title","job_type","experience","location","status")

@admin.register(SavedJob)
class SavedJobAdmin(admin.ModelAdmin):
    list_display = ("candidate", "job", "saved_at")
