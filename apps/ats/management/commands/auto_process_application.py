from django.core.management.base import BaseCommand
from apps.jobs.models import JobApplication
from services.ats_engine import process_application


class Command(BaseCommand):
    help = "Auto process applications"

    def handle(self, *args, **kwargs):
        applications = JobApplication.objects.filter(status='applied')

        for app in applications:
            process_application(app)

        self.stdout.write("Auto processing completed")