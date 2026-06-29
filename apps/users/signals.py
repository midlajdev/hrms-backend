from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User, EmployerProfile, CandidateProfile


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:

        if instance.role == 'employer':
            EmployerProfile.objects.create(user=instance)

        elif instance.role == 'candidate':
            CandidateProfile.objects.create(user=instance)