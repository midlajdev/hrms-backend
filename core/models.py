from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
# class User(models.Model):
#     name = models.CharField(max_length=60)
#     email = models.EmailField(unique=True)
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#             return self.name

# class Job(models.Model):
#     title = models.CharField(max_length=50)
#     description = models.CharField(max_length=255)
#     posted_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#             return self.title

# class Application(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     job = models.ForeignKey(Job, on_delete= models.CASCADE)
#     applied_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#             return f"{self.user.name} - {self.job.title}"


class User(AbstractUser):
    ROLE_CHOICE  = (
        ('employer', 'Employer'),
        ('candidate', 'Candidate')
    )

    role = models.CharField(max_length=20, choices=ROLE_CHOICE, default='candidate')
    
    def __str__(self):
        return self.username

class Employer(models.Model):
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

    def __str__(self):
        return self.company_name
    
class Candidate(models.Model):
    EXPERIENCE_LEVEL_CHOICES = (
        ('fresher', 'Fresher'),
        ('junior', 'Junior'),
        ('mid', 'Mid-Level'),
        ('senior', 'Senior'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='candidate_profile')
    phone = models.CharField(max_length=15, blank=True, null=True)
    resume = models.FileField(upload_to='resumes/', blank=True, null=True)
    skills = models.TextField(blank=True, null=True)
    total_experience = models.FloatField(help_text="Years of experience", blank=True, null=True)
    current_company = models.CharField(max_length=255, blank=True, null=True)
    current_salary = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    expected_salary = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    linkedin_url = models.URLField(blank=True, null=True)
    github_url = models.URLField(blank=True, null=True)
    portfolio_url = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username
    
class Job(models.Model):
    JOB_TYPE_CHOICES = (
        ('full_time', 'Full Time'),
        ('part_time', 'Part Time'),
        ('internship', 'Internship'),
        ('contract', 'Contract'),
    )
    EXPERIENCE_REQUIRED_CHOICES = (
        ('fresher', 'Fresher'),
        ('1-3', '1-3 Years'),
        ('3-5', '3-5 Years'),
        ('5+', '5+ Years'),
    )
    employer = models.ForeignKey(Employer, on_delete=models.CASCADE, related_name='jobs')
    title = models.CharField(max_length=255)
    description = models.TextField()
    location = models.CharField(max_length=255)
    job_type = models.CharField(max_length=20, choices=JOB_TYPE_CHOICES)
    experience_required = models.CharField(max_length=20, choices=EXPERIENCE_REQUIRED_CHOICES)
    salary = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    skills_required = models.TextField()
    application_deadline = models.DateField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        
    def __str__(self):
        return self.title
    
class Application(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='applications')
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, related_name='applications')
    applied_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('job', 'candidate')
        ordering = ['-applied_at']

    def __str__(self):
        return f"{self.candidate.user.username} - {self.job.title}" 