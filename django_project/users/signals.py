from django.db.models.signals import post_save
from django.contrib.auth.models import User, Group
from django.dispatch import receiver
from .models import Profile, extendedUser


@receiver(post_save, sender=extendedUser)
def create_profile(sender, instance, created, **kwargs):
    if created:
        # Make by default every new user a patient
        if instance.type == 'NN' or instance.type == 'PT':
            instance.groups.add(Group.objects.get(name='Patient'))
        elif instance.type == 'MD':
            instance.groups.add(Group.objects.get(name='Medic'))
        Profile.objects.create(user=instance)


@receiver(post_save, sender=extendedUser)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()
