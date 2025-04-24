from django.db import models
from django.contrib.auth.models import AbstractUser

# Custom foydalanuvchi modeli
class User(AbstractUser):
    ROLE_CHOICES = (
        ('student', 'Student'),
        ('instructor', 'Instructor'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='student')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username

# O‘qituvchi profili
class Instructor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='instructor_profile')
    bio = models.TextField(blank=True)
    profile_pic = models.ImageField(upload_to='instructors/', blank=True, null=True)

    def __str__(self):
        return f"Instructor: {self.user.username}"
