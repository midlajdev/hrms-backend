from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from apps.users.permissions import IsEmployer, IsCandidate, IsAdmin
from apps.jobs.serializers import JobSerializer, JobListSerializer, JobApplicationSerializer, SavedJobSerializer, JobDetailSerializer
from rest_framework import generics
from rest_framework.permissions import AllowAny
from .models import Job, EmployerProfile
from utils.pagination import CustomPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from utils.filters import JobFilter
from apps.applications.models import JobApplication
from apps.jobs.models import SavedJob
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.utils.timezone import now, timedelta
from utils.adminLog import log_admin_action
from django.core.cache import cache
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

User = get_user_model()


# Create your views here.
class JobCreateView(generics.CreateAPIView):
    serializer_class = JobSerializer
    permission_classes = [IsAuthenticated, IsEmployer]

    def perform_create(self, serializer):
        employer = EmployerProfile.objects.get(
            user=self.request.user
        )
        serializer.save(employer=employer)
    
class JobStatusToggleView(APIView):
    permission_classes = [IsAuthenticated, IsEmployer]

    def patch(self, request, pk):
        employer = EmployerProfile.objects.get(user=request.user)
        job = Job.objects.get(pk=pk, employer=employer)
        if job.status == "active":
            job.status = "inactive"
        else:
            job.status = "active"

        job.save()
        return Response(
            {"message": "Job status updated", "status": job.status},
            status=status.HTTP_200_OK
        )


@method_decorator(cache_page(60), name='dispatch')
class JobListView(generics.ListAPIView):
    queryset = Job.objects.select_related('employer').filter(status='active',approval_status='approved',is_removed_by_admin=False,employer__user__is_active=True)
    pagination_class = CustomPagination
    serializer_class = JobListSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = JobFilter
    search_fields = ["title", "description", "skills"]

class JobDetailView(generics.RetrieveAPIView):
    queryset = Job.objects.select_related('employer').filter(
        status='active',
        approval_status='approved',
        is_removed_by_admin=False,
        employer__user__is_active=True
    )
    serializer_class = JobDetailSerializer
    permission_classes = [AllowAny]

@method_decorator(cache_page(60), name='dispatch')
class FeaturedJobListView(generics.ListAPIView):
    serializer_class = JobListSerializer
    permission_classes = [AllowAny]
    pagination_class = CustomPagination
    def get_queryset(self):
        return Job.objects.filter( is_featured=True,status='active',approval_status='approved',is_removed_by_admin=False,employer__user__is_active=True).select_related('employer')

@method_decorator(cache_page(60), name='dispatch') 
class LatestJobListView(generics.ListAPIView):
    serializer_class = JobListSerializer
    permission_classes = [AllowAny]
    def get_queryset(self):
        return Job.objects.filter(
            status='active',approval_status='approved',is_removed_by_admin=False,employer__user__is_active=True
        ).select_related('employer').order_by("-created_at")[:10]

class EmployerJobListView(generics.ListAPIView):
    serializer_class = JobSerializer
    permission_classes = [IsAuthenticated, IsEmployer]
    def get_queryset(self):
        return Job.objects.filter(employer__user=self.request.user)
    
class JobUpdateView(generics.UpdateAPIView):
    serializer_class = JobSerializer
    permission_classes = [IsAuthenticated, IsEmployer]
    def get_queryset(self):
        employer = EmployerProfile.objects.get(
            user=self.request.user
        )
        return Job.objects.filter(employer=employer)
    
class CloseJobView(generics.UpdateAPIView):
    serializer_class = JobSerializer
    permission_classes = [IsAuthenticated, IsEmployer]
    def get_queryset(self):
        return Job.objects.filter(employer__user=self.request.user)
    
    def perform_update(self, serializer):
        serializer.save(status="closed")

class CandidateDashboardView(APIView):
    permission_classes = [IsAuthenticated, IsCandidate]

    def get(self, request):
        user = self.request.user
        cache_key = f"dashboard_{user.id}"

        data = cache.get(cache_key)

        if not data:
            print("FROM DB")  # for testing

            applied_jobs = JobApplication.objects.filter(candidate__user=user).select_related('job', 'job__employer')
            saved_jobs = SavedJob.objects.filter(candidate=user).select_related('job')
            interview_jobs = applied_jobs.filter(status='interview')
            rejected_jobs = applied_jobs.filter(status='rejected')
            shortlisted_jobs = applied_jobs.filter(status='shortlisted')


            data = {
                "applied_jobs": JobApplicationSerializer(applied_jobs, many=True).data,
                "saved_jobs": SavedJobSerializer(saved_jobs, many=True).data,
                "interview_jobs": JobApplicationSerializer(interview_jobs, many=True).data,
                "rejected_jobs":JobApplicationSerializer(rejected_jobs, many=True).data,
                "shortlisted_jobs":JobApplicationSerializer(shortlisted_jobs, many=True).data

            }
            cache.set(cache_key, data, timeout=60)
        
        else:
            print("FROM CACHE")
        return Response(data)
    
class SaveJobView(generics.CreateAPIView):
    serializer_class = SavedJobSerializer
    permission_classes = [IsAuthenticated, IsCandidate]

    def perform_create(self, serializer):
        serializer.save(candidate=self.request.user)


class RemoveSavedJobView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated, IsCandidate]

    def get_object(self):
        return get_object_or_404(
            SavedJob,
            candidate=self.request.user,
            job_id=self.kwargs['job_id']
        )

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)

        return Response(
            {"message": "Removed successfully"},
            status=status.HTTP_200_OK
        )
    
class ApplicationTrackingView(generics.RetrieveAPIView):
    serializer_class = JobApplicationSerializer
    permission_classes = [IsAuthenticated, IsCandidate]

    def get_object(self):
        return JobApplication.objects.get(
            id=self.kwargs['pk'],
            candidate__user=self.request.user
        )
    
class RecommendedJobsView(APIView):
    permission_classes = [IsAuthenticated, IsCandidate]

    def get(self, request):
        user = request.user
        profile = user.candidate_profile
        if not profile.skills:
            return Response({"jobs": []})
        skills = [skill.strip() for skill in profile.skills.split(',') if skill.strip()]
        if not skills:
            return Response({"jobs": []})
        # Basic filtering (first skill)
        query = Q()
        for skill in skills:
            query |= Q(skills__icontains=skill)
        jobs = Job.objects.filter(query).distinct()

        return Response(JobSerializer(jobs, many=True).data)
    
class JobModerationView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def patch(self, request, job_id):
        job = Job.objects.get(id=job_id)
        action = request.data.get("action")

        if action == "approved":
            job.approval_status = "approved"
            job.save()
            log_admin_action(
                admin=request.user,
                action="Job Approved",
                target_type="Job",
                target_id=job.id,
            )
        elif action == "reject":
            job.approval_status = "rejected"
            job.save()
            log_admin_action(
                admin=request.user,
                action="Job Rejected",
                target_type="Job",
                target_id=job.id,
            )
        else:
            return Response({"error": "Invalid action"}, status=400)
        return Response({"message": f"Job {job.approval_status}"})
    
class AdminStatsView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def get(self, request):
        total_users = User.objects.count()
        total_jobs = Job.objects.count()
        total_applications = JobApplication.objects.count()

        last_7_days_users = User.objects.filter(
            date_joined__gte=now() - timedelta(days=7)
        ).count()

        return Response({
            "total_users": total_users,
            "total_jobs": total_jobs,
            "total_applications": total_applications,
            "new_users_last_7_days": last_7_days_users
        })
        
class RemoveSpamJobView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]
    def patch(self, request, job_id):
        job = Job.objects.get(id=job_id)
        job.is_removed_by_admin = True
        job.save()
        log_admin_action(
                admin=request.user,
                action="Job Removed",
                target_type="job",
                target_id=job.id,
            )
        return Response({"message": "Job removed by admin"})