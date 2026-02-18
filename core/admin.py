from django.contrib import admin
from .models import User, Job,Application, Employer, Candidate
# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "email","role")

@admin.register(Employer)
class EmployerAdmin(admin.ModelAdmin):
    list_display = ("user","company_name","industry", "company_location")
    search_fields = ("company_name", "industry")

@admin.register(Candidate)
class CandidateAdmin(admin.ModelAdmin):
    list_display = ("user", "resume", "phone", "linkedin_url")

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ("employer","title","location","created_at")
    list_filter = ("job_type", "experience_required")
    search_fields = ("title",)

@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ("job","candidate", "applied_at")
    search_fields = ("job__title",)
