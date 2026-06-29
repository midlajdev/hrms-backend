from rest_framework.views import APIView
from rest_framework.response import Response
from apps.users.permissions import IsAdmin, IsEmployer
from apps.users.models import User, EmployerProfile
from apps.users.serializers import EmployerProfileSerializer
from apps.jobs.models import Job
from apps.applications.models import JobApplication
from apps.applications.serializers import RecentApplicationSerializer

class AnalyticsView(APIView):
    permission_classes = [IsAdmin]

    def get(self, request):
        total_candidates = User.objects.filter(role='candidate').count()
        total_employers = User.objects.filter(role='employer').count()
        total_jobs = Job.objects.count()
        total_applications = JobApplication.objects.count()

        return Response({
            'total_candidates': total_candidates,
            'total_employers': total_employers,
            'total_jobs': total_jobs,
            'total_applications':total_applications
        })

class EmployersListView(APIView):
    permission_classes = [IsAdmin]

    def get(self, request):
        employers = EmployerProfile.objects.select_related('user').all()
        serializer = EmployerProfileSerializer(employers, many=True)
        return Response(serializer.data)

class EmployerAnalyticsView(APIView):
    permission_classes = [IsEmployer]

    def get(self, request):
        employer_profile = request.user.employer_profile
        total_jobs = Job.objects.filter(employer=employer_profile).count()
        total_applications = JobApplication.objects.filter(job__employer=employer_profile).count()
        total_shortlisted = JobApplication.objects.filter(job__employer=employer_profile, status='shortlisted').count()

        return Response({
            'total_jobs_posted': total_jobs,
            'total_applications_received': total_applications,
            'total_shortlisted_candidates': total_shortlisted
        })

class RecentApplicationsView(APIView):
    permission_classes = [IsEmployer]

    def get(self, request):
        employer_profile = request.user.employer_profile
        applications = JobApplication.objects.filter(job__employer=employer_profile).select_related('candidate__user', 'job').order_by('-applied_date')[:4]
        serializer = RecentApplicationSerializer(applications, many=True)
        return Response(serializer.data)