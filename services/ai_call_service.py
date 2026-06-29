from celery import shared_task
from apps.applications.models import JobApplication


@shared_task(bind=True, max_retries=3)
def trigger_ai_call(self, application_id):

    try:
        application = JobApplication.objects.get(id=application_id)

        application.ai_call_status = "queued"
        application.save()

        # simulate API call
        print("AI service called")

    except Exception as e:

        application.ai_call_status = "failed"
        application.ai_retry_count += 1
        application.save()

        raise self.retry(exc=e, countdown=300)
    

