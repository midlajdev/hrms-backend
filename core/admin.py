# @admin.register(Job)
# class JobAdmin(admin.ModelAdmin):
#     list_display = ("employer","title","location","created_at")
#     list_filter = ("job_type", "experience_required")
#     search_fields = ("title",)

# @admin.register(Application)
# class ApplicationAdmin(admin.ModelAdmin):
#     list_display = ("job","candidate", "applied_at")
#     search_fields = ("job__title",)
