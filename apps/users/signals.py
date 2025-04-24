from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User, Instructor

@receiver(post_save, sender=User)
def create_instructor_profile(sender, instance, created, **kwargs):
    if created and instance.role == 'instructor':
        Instructor.objects.create(user=instance)
