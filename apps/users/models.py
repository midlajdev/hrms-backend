from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import UserManager
# Create your models here.
class User(AbstractUser):

    username = None

    ROLE_CHOICES  = (
        ('admin', 'Admin'),
        ('employer', 'Employer'),
        ('candidate', 'Candidate')
    )

    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='candidate')
    is_verified = models.BooleanField(default=False)

    is_flagged = models.BooleanField(default=False)
    flag_count = models.IntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email
    
class EmployerProfile(models.Model):
    COMPANY_SIZE_CHOICES = (
        ('1-10', '1-10 Employees'),
        ('11-50', '11-50 Employees'),
        ('51-200', '51-200 Employees'),
        ('201-500', '201-500 Employees'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='employer_profile')
    company_name = models.CharField(max_length=255)
    industry = models.CharField(max_length=255, blank=True, null=True)
    founded_year = models.PositiveIntegerField(blank=True, null=True)
    company_location = models.CharField(max_length=255)
    company_website = models.URLField(blank=True, null=True)
    company_description = models.TextField(blank=True, null=True)
    logo = models.ImageField(upload_to='company_logos/', blank=True, null=True)
    company_size = models.CharField(max_length=20, choices=COMPANY_SIZE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.company_name
    

def resume_upload_path(instance, filename):
    return f"resumes/candidate_{instance.user.id}/{filename}"

class CandidateProfile(models.Model):
    EXPERIENCE_LEVEL_CHOICES = (
        ('fresher', 'Fresher'),
        ('junior', 'Junior'),
        ('mid', 'Mid-Level'),
        ('senior', 'Senior'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='candidate_profile')
    first_name = models.CharField(max_length=25, blank=True,null=True)
    last_name = models.CharField(max_length=25,blank=True,null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    resume = models.FileField(upload_to=resume_upload_path, blank=True, null=True)
    skills = models.TextField(blank=True, null=True)
    highest_education = models.CharField(max_length=255, blank=True, null=True)
    total_experience = models.FloatField(help_text="Years of experience", blank=True, null=True)
    experience_level = models.CharField(max_length=30, choices=EXPERIENCE_LEVEL_CHOICES, blank=True, null=True)
    current_company = models.CharField(max_length=255, blank=True, null=True)
    current_salary = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    expected_salary = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    linkedin_url = models.URLField(blank=True, null=True)
    github_url = models.URLField(blank=True, null=True)
    portfolio_url = models.URLField(blank=True, null=True)
    location = models.CharField(max_length=75, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    is_active = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [models.Index(fields=["location"]),]

    def __str__(self):
        return self.user.email
    

class AdminActionLog(models.Model):
    admin = models.ForeignKey(User, on_delete=models.CASCADE)
    action = models.CharField(max_length=255)
    target_type = models.CharField(max_length=50)  # User / Job / Employer
    target_id = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.admin.email} - {self.action}"