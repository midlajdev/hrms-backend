from django.db import models
from apps.users.models import CandidateProfile
from apps.jobs.models import Job
from apps.users.models import User
# Create your models here.
class JobApplication(models.Model):

    STATUS_CHOICES = [
        ('applied', 'Applied'),
        ('shortlisted', 'Shortlisted'),
        ('interview', 'Interview Scheduled'),
        ('hired', 'Hired'),
        ('rejected', 'Rejected'),
        ('selected', 'Selected')
    ]

    AI_CALL_STATUS = [
        ('not_triggered', 'Not Triggered'),
        ('queued', 'Queued'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]

    candidate = models.ForeignKey( CandidateProfile, on_delete=models.CASCADE, related_name='applications')
    job = models.ForeignKey( Job, on_delete=models.CASCADE, related_name='applications')
    resume_snapshot = models.FileField(upload_to='application_resumes/')
    status = models.CharField( max_length=20,choices=STATUS_CHOICES,default='applied')
    applied_date = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    ats_score = models.FloatField(default=0)
    is_manual_override = models.BooleanField(default=False)

    ai_call_status = models.CharField(max_length=20, choices=AI_CALL_STATUS, default='not_triggered')
    ai_retry_count = models.IntegerField(default=0)
    ai_call_scheduled_at = models.DateTimeField(null=True, blank=True)
    ai_call_completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ['candidate', 'job']
        indexes = [
        models.Index(fields=['job', 'status']),          
        models.Index(fields=['candidate']),              
        models.Index(fields=['applied_date']),           
        models.Index(fields=['ats_score']),              
    ]
    
    def __str__(self):
        return f"candidate - {self.candidate} applied for {self.job.title}"

class ApplicationStatusLog(models.Model):
    application = models.ForeignKey( JobApplication, on_delete=models.CASCADE, related_name='status_logs')
    old_status = models.CharField(max_length=20)
    new_status = models.CharField(max_length=20)
    changed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    changed_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        indexes = [
            models.Index(fields=['application']),
            models.Index(fields=['changed_at']),
        ]
        
    def __str__(self):
        return f"{self.application} : {self.old_status} → {self.new_status}"



class AIInterviewSession(models.Model):

    STATUS_CHOICES = (
        ("started", "Started"),
        ("completed", "Completed"),
        ("failed", "Failed"),
    )

    candidate = models.ForeignKey(User, on_delete=models.CASCADE)
    job = models.ForeignKey(Job,on_delete=models.CASCADE)
    triggered_by = models.ForeignKey(User,on_delete=models.SET_NULL,null=True,related_name="triggered_sessions")
    status = models.CharField(max_length=20,choices=STATUS_CHOICES,default="started")
    ai_model_used = models.CharField(max_length=100,default="GPT")
    started_at = models.DateTimeField(auto_now_add=True)
    ended_at = models.DateTimeField(null=True,blank=True)

    def __str__(self):
        return f"{self.candidate.email}"
    


class AIQuestion(models.Model):

    session = models.ForeignKey(AIInterviewSession,on_delete=models.CASCADE,related_name="questions")
    question_text = models.TextField()
    question_order = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.question_text[:50]
    
class AIAnswer(models.Model):

    question = models.ForeignKey( AIQuestion,on_delete=models.CASCADE,related_name="answers")
    answer_text = models.TextField()
    transcript_json = models.JSONField(default=dict)
    confidence_score = models.FloatField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

class CallLog(models.Model):

    STATUS = (
        ("connected", "Connected"),
        ("disconnected", "Disconnected"),
        ("failed", "Failed"),
    )

    session = models.ForeignKey(AIInterviewSession,on_delete=models.CASCADE,related_name="call_logs")
    call_status = models.CharField(max_length=30,choices=STATUS)
    duration = models.IntegerField(default=0)
    disconnect_reason = models.TextField(blank=True,null=True)
    started_at = models.DateTimeField(blank=True, null=True)
    ended_at = models.DateTimeField(null=True,blank=True)