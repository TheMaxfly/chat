

# Create your models here.
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

class TemporaryConversation(models.Model):
    name = models.CharField(max_length=255, unique=True)
    client = models.ForeignKey(User, related_name='client_conversations', on_delete=models.CASCADE)
    advisor = models.ForeignKey(User, related_name='advisor_conversations', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

class Message(models.Model):
    conversation = models.ForeignKey(TemporaryConversation, related_name='messages', on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)





class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_advisor = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} Profile"




@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


   
