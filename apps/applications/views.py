from rest_framework import generics
from rest_framework.views import APIView
from .models import CandidateProfile, JobApplication, ApplicationStatusLog
from .serializers import ApplyJobSerializer, JobAppliedSerializer, ApplicationStatusUpdateSerializer, ApplicantSerializer
from apps.users.permissions import IsCandidate
from rest_framework.permissions import IsAuthenticated
from rest_framework.serializers import ValidationError
from apps.users.permissions import IsEmployer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.response import Response
from rest_framework import status
from apps.users.serializers import ResumeUploadSerializer
from utils.resume_parser import extract_text_from_pdf, extract_text_from_docx, clean_text, parse_resume_from_text
from services.ats_scoring import calculate_total_score
from services.ats_engine import process_application
from services.notification_email import notify_application_submitted
from django.db.models import Count, Q


# Create your views here.

VALID_TRANSITIONS = {
    'applied': ['shortlisted', 'rejected'],
    'shortlisted': ['interview'],
    'interview': ['selected', 'rejected'],
}

class ApplyJobView(generics.CreateAPIView):
    serializer_class = ApplyJobSerializer
    permission_classes = [IsAuthenticated, IsCandidate]

    def perform_create(self, serializer):
        candidate = CandidateProfile.objects.get(user=self.request.user)
        job = serializer.validated_data['job']
        ats_score = calculate_total_score(job, candidate)
        # duplicate prevention
        if JobApplication.objects.filter(candidate=candidate, job=job).exists():
            raise ValidationError("You already applied for this job")
        # resume selection
        resume = serializer.validated_data.get('resume_snapshot')
        if not resume:
            if not candidate.resume:
                raise ValidationError("Please upload a resume in your profile")
            resume = candidate.resume

        application = serializer.save(candidate=candidate, resume_snapshot=resume,ats_score= ats_score)
        notify_application_submitted(application)
        process_application(application)
        
        print("ATS SCORE:", application.ats_score)
        print("FINAL STATUS:", application.status)

class MyApplicationsView(generics.ListAPIView):
    serializer_class = JobAppliedSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        candidate = CandidateProfile.objects.get(user=self.request.user)
        return JobApplication.objects.filter(candidate=candidate).select_related('job', 'job__employer')
    
class UpdateApplicationStatusView(generics.UpdateAPIView):
    serializer_class = ApplicationStatusUpdateSerializer
    permission_classes = [IsAuthenticated, IsEmployer]

    def get_queryset(self):
        return JobApplication.objects.filter(job__employer__user=self.request.user)

    def perform_update(self, serializer):
        application = self.get_object()
        old_status = application.status
        new_status = serializer.validated_data.get('status')

        # Validate transition
        if old_status in VALID_TRANSITIONS:
            if new_status not in VALID_TRANSITIONS[old_status]:
                raise ValidationError("Invalid status transition")
        serializer.save(is_manual_override=True)
        ApplicationStatusLog.objects.create(
            application=application,
            old_status=old_status,
            new_status=new_status,
            changed_by=self.request.user
        )

class ApplicantListView(generics.ListAPIView):
    serializer_class = ApplicantSerializer
    permission_classes = [IsAuthenticated, IsEmployer]
    filter_backends = [DjangoFilterBackend, SearchFilter]

    filterset_fields = ['status']
    search_fields = ['candidate__user__email']

    def get_queryset(self):
        job_id = self.kwargs['job_id']
        return JobApplication.objects.filter(
            job__id=job_id,
            job__employer__user=self.request.user
        ).select_related('candidate__user','job')

class JobAnalyticsView(APIView):
    permission_classes = [IsAuthenticated, IsEmployer]
    def get(self, request, job_id):
        data = JobApplication.objects.filter(
            job__id=job_id,
            job__employer__user=request.user
        ).aggregate(
            total=Count('id'),
            shortlisted=Count('id', filter=Q(status='shortlisted'))
        )
        total = data['total']
        shortlisted = data['shortlisted']

        ratio = 0
        if total > 0:
            ratio = shortlisted / total

        return Response({
            "total_applications": total,
            "shortlisted": shortlisted,
            "shortlist_ratio": ratio
        })
    
    
class ResumeParseView(APIView):
     def post(self, request):
        serializer = ResumeUploadSerializer(data=request.data)

        if serializer.is_valid():
            file = serializer.validated_data['resume']
            filename = file.name.lower()

            if filename.endswith('.pdf'):
                text = extract_text_from_pdf(file)
            elif filename.endswith('.docx'):
                text = extract_text_from_docx(file)
            else:
                return Response({"error": "Unsupported file format"}, status=400)

            cleaned_text = clean_text(text)

            parsed_data = parse_resume_from_text(cleaned_text)

            return Response({
                "parsed_data": parsed_data
            })

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)