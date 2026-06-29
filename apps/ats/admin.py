from django.contrib import admin
from apps.ats.models import ATSScore
# Register your models here.
@admin.register(ATSScore)
class ATSScoreAdmin(admin.ModelAdmin):
    list_display = ("candidate","job","score")