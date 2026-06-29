import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from apps.jobs.models import Job
from apps.users.models import User, CandidateProfile
from unittest.mock import patch
from django.core.files.uploadedfile import SimpleUploadedFile
from apps.users.models import EmployerProfile


@pytest.mark.django_db
def test_job_creation():
    user = User.objects.create_user(
        email="emp@test.com",
        password="Test@1234",
        role="employer"
    )

    client = APIClient()
    client.force_authenticate(user=user)

    response = client.post(reverse('job-create'), {
        "title": "Backend Developer",
        "description": "Django job",
        "location": "Remote",
        "skills": "django, drf, api",
        "qualification": "MCA, BTech"
    })

    assert response.status_code == 201
    assert Job.objects.count() == 1


@pytest.mark.django_db
@patch('apps.applications.views.calculate_total_score', return_value=80)
@patch('apps.applications.views.notify_application_submitted')
@patch('apps.applications.views.process_application')
def test_apply_job(mock_process, mock_notify, mock_score):
    
    candidate_user = User.objects.create_user(
        email="c@test.com",
        password="Test@1234",
        role="candidate"
    )

    employer_user = User.objects.create_user(
        email="emp@test.com",
        password="Test@1234",
        role="employer"
    )
    employer_profile = EmployerProfile.objects.get(user=employer_user)

    resume = SimpleUploadedFile("resume.pdf", b"file_content")

    candidate = CandidateProfile.objects.get(user=candidate_user)
    candidate.resume = resume
    candidate.save()

    job = Job.objects.create(
        title="Test Job",
        description="Test desc",
        location="Remote",
        skills="django",
        qualification="MCA",
        employer=employer_profile
    )

    client = APIClient()
    client.force_authenticate(user=candidate_user)

    response = client.post(
        reverse('apply-job'),
        {"job": job.id}
    )

    assert response.status_code == 201