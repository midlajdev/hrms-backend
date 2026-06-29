from rest_framework import serializers
from apps.jobs.models import Job, SavedJob
from apps.applications.models import JobApplication

class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = "__all__"
        read_only_fields = [
            "id",
            "employer",
            "status",
            "created_at",
            "updated_at"
        ]
    def validate(self, data):
        salary_min = data.get("salary_min")
        salary_max = data.get("salary_max")

        if salary_min is not None and salary_max is not None:
            if salary_min > salary_max:
                raise serializers.ValidationError(
                    "Minimum salary cannot be greater than maximum salary"
                )
        return data

class JobListSerializer(serializers.ModelSerializer):
    company = serializers.CharField(source="employer.company_name")

    class Meta:
        model = Job
        fields = [
            "id",
            "title",
            "company",
            "location",
            "experience",
            "salary_min",
            "salary_max",
            "job_type",
            "created_at"
        ]

class JobDetailSerializer(serializers.ModelSerializer):
    company = serializers.CharField(source="employer.company_name")
    employer_user_id = serializers.IntegerField(source="employer.user.id", read_only=True)

    class Meta:
        model = Job
        fields = [
            "id",
            "title",
            "company",
            "employer_user_id",
            "description",
            "qualification",
            "skills",
            "location",
            "experience",
            "salary_min",
            "salary_max",
            "job_type",
            "created_at"
        ]
        
# for candidate dashboard view
class JobApplicationSerializer(serializers.ModelSerializer):
    job = JobSerializer(read_only=True)

    class Meta:
        model = JobApplication
        fields = [
            'id',
            'job',
            'status',
            'applied_date',
            'updated_at'
        ]

class SavedJobSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavedJob
        fields = ['id', 'job', 'saved_at']