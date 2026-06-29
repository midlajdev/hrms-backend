from django.contrib import admin
from apps.users.models import User,EmployerProfile, CandidateProfile, AdminActionLog
from django.contrib.auth.admin import UserAdmin

# Register your models here.
# @admin.register(User)
# class UserAdmin(admin.ModelAdmin):
#     list_display = ("email","role")

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ("id", "email", "role", "is_staff", "is_active")
    list_filter = ("role", "is_staff", "is_active")

    ordering = ("email",)
    search_fields = ("email",)

    fieldsets = (
        (None, {"fields": ("email", "password","is_flagged","flag_count")}),
        ("Permissions", {"fields": ("role", "is_staff", "is_active", "is_superuser")}),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "password1", "password2", "role"),
        }),
    )

@admin.register(EmployerProfile)
class EmployerAdmin(admin.ModelAdmin):
    list_display = ("id","user","company_name","industry", "company_location", "is_approved")
    search_fields = ("company_name", "industry")

@admin.register(CandidateProfile)
class CandidateAdmin(admin.ModelAdmin):
    list_display = ("user", "resume", "phone", "location", "linkedin_url", "is_active")

@admin.register(AdminActionLog)
class AdminActionLogAdmin(admin.ModelAdmin):
    list_display = ("admin", "action", "target_type", "target_id")