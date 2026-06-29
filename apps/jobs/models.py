from django.db import models
from django.conf import settings
from apps.users.models import User
from apps.users.models import EmployerProfile, CandidateProfile
# Create your models here.

class Job(models.Model):

    JOB_TYPE_CHOICES = (
        ('full_time', 'Full Time'),
        ('part_time', 'Part Time'),
        ('contract', 'Contract'),
        ('remote', 'Remote'),
    )

    STATUS_CHOICES = (
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('closed', 'Closed'),
    )

    APPROVAL_STATUS = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    )

    employer = models.ForeignKey( EmployerProfile, on_delete=models.CASCADE, related_name="jobs" )
    title = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    skills = models.CharField(max_length=255, help_text="Comma separated skills",blank=True, null=True)
    qualification = models.CharField(max_length=255, blank=True, null=True)
    experience = models.PositiveIntegerField( help_text="Experience in years",blank=True, null=True)
    salary_min = models.DecimalField( max_digits=10, decimal_places=2,blank=True, null=True )
    salary_max = models.DecimalField( max_digits=10, decimal_places=2,blank=True, null=True)
    location = models.CharField(max_length=255,blank=True, null=True)
    job_type = models.CharField( max_length=20, choices=JOB_TYPE_CHOICES,blank=True, null=True )
    status = models.CharField( max_length=10, choices=STATUS_CHOICES, default="active" )
    approval_status = models.CharField(max_length=10, choices=APPROVAL_STATUS, default='approved')
    
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_removed_by_admin = models.BooleanField(default=False)

    shortlist_threshold = models.FloatField(default=70)
    reject_threshold = models.FloatField(default=30)
    auto_shortlist = models.BooleanField(default=True)
    auto_reject = models.BooleanField(default=True)
    class Meta:
        indexes = [
            models.Index(fields=['status']),
            models.Index(fields=['approval_status']),
            models.Index(fields=['employer']),
            models.Index(fields=['created_at']),
            models.Index(fields=['is_featured']),
        ]
    def __str__(self):
        return f"{self.employer.company_name} - {self.title}"
    

class SavedJob(models.Model):
    candidate = models.ForeignKey(User, on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    saved_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['candidate', 'job']
        indexes = [
            models.Index(fields=['candidate']),
        ]
