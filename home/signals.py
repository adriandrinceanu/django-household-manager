from django.db.models.signals import post_save
from django.dispatch import receiver
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .models import Chore, Notification, Expense, Member
import logging
logger = logging.getLogger(__name__)



            
@receiver(post_save, sender=Chore)
def create_chore_notification(sender, instance, created, **kwargs):
    logger.info(f"Creating chore notification for {instance}")
    if created:
        # Get the member who created the chore
        creator_member = Member.objects.get(user=instance.created_by)
        notification = Notification.objects.create(
            user=instance.created_by,
            member=creator_member,  # Set the member field
            message=f"{instance.created_by.member.name} assigned the chore: {instance.title} to {instance.assigned_to.name}.",
            family=instance.assigned_to.family,
            chore=instance  # Set the chore field
        )
        # Send notification to family's group
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f"notifications_{instance.assigned_to.family.id}",
            {
                "type": "send_notification",
                "text": str(notification),
            }
        )
        
