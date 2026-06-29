from apps.applications.models import JobApplication


def trigger_ai_call(application_id):

    try:
        application = JobApplication.objects.get(id=application_id)

        application.ai_call_status = "queued"
        application.save()

        # simulate API call
        print("AI service called")

    except Exception:

        application.ai_call_status = "failed"
        application.ai_retry_count += 1
        application.save()

        raise
    

