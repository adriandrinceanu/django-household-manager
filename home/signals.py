from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Chore, Notification, Expense

# @receiver(post_save, sender=Chore)
# def create_notification(sender, instance, created, **kwargs):
#     if created:
#         Notification.objects.create(
#             user=instance.assigned_to.user,
#             message=f"You have been assigned a new chore: {instance.title}",
#             family=instance.assigned_to.family,  # this should now work
#             member=instance.assigned_to,
#             chore=instance,
#         )

@receiver(post_save, sender=Chore)
def create_chore_notification(sender, instance, created, **kwargs):
    if created:
        # Get all members of the family
        family_members = instance.assigned_to.family.family_members.all()
        
        # Create a notification for each member
        for member in family_members:
            Notification.objects.create(
                user=member.user,
                message=f"{instance.created_by.member.name} assigned the chore: {instance.title} to {instance.assigned_to.name}.",
                family=instance.assigned_to.family,
            )
            
            
# 'NoneType' object has no attribute 'user' - error           
# @receiver(post_save, sender=Expense)
# def create_expense_notification(sender, instance, created, **kwargs):
#     if created:
#         # Get the names of all members who created the expense
#         members = ", ".join([member.name for member in instance.created_by.all()])
#         Notification.objects.create(
#             user=instance.created_by.first().user,  # Assuming you want to send the notification to the first member
#             message=f"{members} spent {instance.amount} on {instance.category}.",
#             family=instance.created_by.first().family,  # Assuming all members belong to the same family
#         )


#untested, might work:
# @receiver(post_save, sender=Expense)
# def create_expense_notification(sender, instance, created, **kwargs):
#     if created:
#         for member in instance.created_by.all():
#             Notification.objects.create(
#                 user=member.user,
#                 message=f"{member.name} spent {instance.amount} on {instance.category}.",
#                 family=member.family,
#             )