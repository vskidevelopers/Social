from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profiles, Friendship

@receiver(post_save, sender=User)
def post_save_create_user(sender, instance, created, **kwargs):
    if created:
        Profiles.objects.create(user=instance)

@receiver(post_save, sender=Friendship)
def post_save_add_friends(sender, instance, created, **kwargs):
    request_sender = instance.sender
    request_receiver= instance.receiver
    if instance.friendship_status == "accepted":
        request_sender.friends.add(request_receiver.user)
        request_receiver.friends.add(request_sender.user)
        request_sender.save()
        request_receiver.save()