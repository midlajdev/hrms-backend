from django.db.models import Count
from django.core.cache import cache

from apps.jobs.models import Job
from apps.applications.models import JobApplication


class AnalyticsService:

    def get_job_analytics(self, job):

        cache_key = f"analytics_job_{job.id}"

        cached = cache.get(cache_key)

        if cached:
            return cached

        applications = JobApplication.objects.filter(
            job=job
        )

        total = applications.count()

        shortlisted = applications.filter(
            status="shortlisted"
        ).count()

        interviewed = applications.filter(
            status="interview"
        ).count()

        selected = applications.filter(
            status="selected"
        ).count()

        hired = applications.filter(
            status="hired"
        ).count()

        analytics = {

            "job": job.title,

            "total_applications": total,

            "shortlisted": shortlisted,

            "interviewed": interviewed,

            "selected": selected,

            "hired": hired,

            "shortlist_ratio": (
                shortlisted / total if total else 0
            ),

            "selection_ratio": (
                selected / total if total else 0
            ),

            "hire_ratio": (
                hired / total if total else 0
            ),
        }

        cache.set(
            cache_key,
            analytics,
            timeout=300
        )

        return analytics