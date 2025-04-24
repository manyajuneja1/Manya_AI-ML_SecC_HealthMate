# App/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from App.views import Profile


@receiver(post_save, sender=User)
def user_created(sender, instance, created, **kwargs):
    if created:
       Profile.objects.create(user=instance) 
