from django.contrib import admin
from apps.notifications.models import EmailLog
# Register your models here.
@admin.register(EmailLog)
class EmailLogAdmin(admin.ModelAdmin):
    list_display = ("email","subject","status","error","created_at")