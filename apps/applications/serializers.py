from rest_framework import serializers
from .models import JobApplication

class ApplyJobSerializer(serializers.ModelSerializer):
    resume_snapshot = serializers.FileField(required=False)
    class Meta:
        model = JobApplication
        fields = ['job', 'resume_snapshot']

    def validate_job(self, value):
        if value.status != 'active':
            raise serializers.ValidationError("Job is not active")
        return value
    
class JobAppliedSerializer(serializers.ModelSerializer):
    job_title = serializers.CharField(source="job.title", read_only=True)
    company = serializers.CharField(source="job.employer.company_name", read_only=True)

    class Meta:
        model = JobApplication
        fields = [
            "id",
            "job_title",
            "company",
            "status",
            "applied_date"
        ]

class ApplicationStatusUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobApplication
        fields = ['status']


class ApplicantSerializer(serializers.ModelSerializer):
    candidate_email = serializers.CharField(source='candidate.user.email', read_only=True)
    candidate_phone = serializers.CharField(source='candidate.phone', read_only=True)
    candidate_name = serializers.SerializerMethodField()
    candidate_resume = serializers.FileField(source='candidate.resume', read_only=True)

    class Meta:
        model = JobApplication
        fields = ['id', 'candidate_name','candidate_email', 'candidate_phone','candidate_resume','status', 'applied_date']
    def get_candidate_name(self, obj):
        first = obj.candidate.first_name or ""
        last = obj.candidate.last_name or ""
        return f"{first} {last}".strip()


class RecentApplicationSerializer(serializers.ModelSerializer):
    candidate_name = serializers.SerializerMethodField()
    candidate_email = serializers.CharField(source='candidate.user.email', read_only=True)
    job_title = serializers.CharField(source='job.title', read_only=True)
    status = serializers.CharField()
    applied_date = serializers.DateTimeField()

    class Meta:
        model = JobApplication
        fields = ['candidate_name', 'candidate_email', 'job_title', 'status', 'applied_date']

    def get_candidate_name(self, obj):
        first = obj.candidate.first_name or ""
        last = obj.candidate.last_name or ""
        return f"{first} {last}".strip()