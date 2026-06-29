from django.db import models

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
    







# class Job(models.Model):
#     JOB_TYPE_CHOICES = (
#         ('full_time', 'Full Time'),
#         ('part_time', 'Part Time'),
#         ('internship', 'Internship'),
#         ('contract', 'Contract'),
#     )
#     EXPERIENCE_REQUIRED_CHOICES = (
#         ('fresher', 'Fresher'),
#         ('1-3', '1-3 Years'),
#         ('3-5', '3-5 Years'),
#         ('5+', '5+ Years'),
#     )
#     employer = models.ForeignKey(Employer, on_delete=models.CASCADE, related_name='jobs')
#     title = models.CharField(max_length=255)
#     description = models.TextField()
#     location = models.CharField(max_length=255)
#     job_type = models.CharField(max_length=20, choices=JOB_TYPE_CHOICES)
#     experience_required = models.CharField(max_length=20, choices=EXPERIENCE_REQUIRED_CHOICES)
#     salary = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
#     skills_required = models.TextField()
#     application_deadline = models.DateField(blank=True, null=True)
#     is_active = models.BooleanField(default=True)
#     created_at = models.DateTimeField(auto_now_add=True)

#     class Meta:
#         ordering = ['-created_at']
        
#     def __str__(self):
#         return self.title
    
# class Application(models.Model):
#     job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='applications')
#     candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, related_name='applications')
#     applied_at = models.DateTimeField(auto_now_add=True)

#     class Meta:
#         unique_together = ('job', 'candidate')
#         ordering = ['-applied_at']

#     def __str__(self):
#         return f"{self.candidate.user.username} - {self.job.title}" 