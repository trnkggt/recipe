from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver

from .models import Profile

@receiver(post_save, sender=User)
def create_profile(sender, created, instance, **kwargs):
    if created:
        Profile.objects.create(user=instance,
                               username=instance.username,
                               email=instance.email)


@receiver(post_save, sender=User)
def update_profile(sender, created, instance, **kwargs):
    if not created:
        instance.profile.save()
