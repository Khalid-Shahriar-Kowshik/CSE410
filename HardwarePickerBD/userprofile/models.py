from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30,null=True ,blank=True)
    last_name = models.CharField(max_length=30, null=True,blank=True)
    phone_number = models.CharField(max_length=15,null=True ,blank=True)
    address = models.TextField(null=True ,blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    bio = models.TextField(null=True ,blank=True)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics/',null=True ,blank=True)

    def __str__(self):
        return f'{self.user.username} Profile'

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()