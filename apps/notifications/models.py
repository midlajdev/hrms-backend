from django.db import models

# Create your models here.
class EmailLog(models.Model):
    email = models.EmailField()
    subject = models.CharField(max_length=255)
    status = models.CharField(max_length=20)
    error = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.email} - {self.status}"