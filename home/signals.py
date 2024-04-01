from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Chore, Notification

@receiver(post_save, sender=Chore)
def create_notification(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            user=instance.assigned_to.user,
            message=f"You have been assigned a new chore: {instance.title}",
            family=instance.assigned_to.family,  # this should now work
            member=instance.assigned_to,
            chore=instance,
        )