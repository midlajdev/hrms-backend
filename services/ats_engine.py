from services.notification_email import notify_shortlisted, notify_rejected
from apps.applications.models import ApplicationStatusLog
from services.ai_eligibility import is_candidate_eligible
from services.ai_call_service import trigger_ai_call


def process_application(application):
    if application.is_manual_override:
        return application.status

    old_status = application.status

    job = application.job
    score = application.ats_score

    if job.auto_shortlist and score >= job.shortlist_threshold:
        application.status = 'shortlisted'

    elif job.auto_reject and score <= job.reject_threshold:
        application.status = 'rejected'

    else:
        application.status = 'applied'

    application.save()
    
    ApplicationStatusLog.objects.create(
        application=application,
        old_status=old_status,
        new_status=application.status,
        changed_by=None  
    )

    if old_status != application.status:
        if application.status == 'shortlisted':
            notify_shortlisted(application)
            if is_candidate_eligible(application):
                trigger_ai_call(application.id)
                
        elif application.status == 'rejected':
            notify_rejected(application)
    return application.status