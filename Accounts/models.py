from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.
class Profile(models.Model):
    ACCOUNT_TYPES = (
        ("advisor", "مستشار"), 
        ("normal", "طبيعي"), 
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    account_type = models.CharField(max_length=20, choices=ACCOUNT_TYPES, default='normal')
    photo = models.ImageField(upload_to='profile/')
    experiences = models.TextField(blank=True, null=True) 
    certificates = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return self.user

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)