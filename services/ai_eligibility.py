def is_candidate_eligible(application):

    # manual override applications should not trigger AI
    if application.is_manual_override:
        return False

    # only shortlisted candidates
    if application.status != "shortlisted":
        return False

    # job must be active
    if application.job.status != "active":
        return False

    # avoid duplicate AI calls
    if application.ai_call_status in [
        "queued",
        "in_progress",
        "completed"
    ]:
        return False

    return True