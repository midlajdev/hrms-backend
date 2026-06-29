from django.shortcuts import render
from apps.users.permissions import IsEmployer
from apps.applications.models import JobApplication
from services.ats_engine import process_application
# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from apps.jobs.models import Job
from apps.users.models import CandidateProfile
from .models import ATSScore
from services.ats_scoring import calculate_total_score
from django.shortcuts import get_object_or_404

class CalculateMatchView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, job_id):
        job = get_object_or_404(Job, id=job_id)

        candidates = CandidateProfile.objects.filter(
            applications__job=job
        ).distinct()

        results = []

        for candidate in candidates:
            score = calculate_total_score(job, candidate)

            ATSScore.objects.update_or_create(
                candidate=candidate,
                job=job,
                defaults={"score": score}
            )

            results.append({
                "candidate_id": candidate.id,
                "score": score
            })

        return Response(results)
    
class RankedCandidatesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, job_id):
        scores = ATSScore.objects.filter(job_id=job_id).order_by('-score')
        data = [
            {
                "candidate_id": s.candidate.id,
                "score": s.score
            }
            for s in scores
        ]

        return Response(data)
    
class AutoProcessView(APIView):
    permission_classes = [IsAuthenticated, IsEmployer]

    def post(self, request, job_id):
        applications = JobApplication.objects.filter(
            job_id=job_id,
            job__employer__user=request.user
        )
        for app in applications:
            score = calculate_total_score(app.job, app.candidate)
            app.ats_score = score
            process_application(app)
            print("ATS SCORE:", app.ats_score)
        return Response({"message": "Applications processed successfully"})