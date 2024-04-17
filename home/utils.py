from .models import Notification

# def create_chore(assigned_to, chore_title, family, chore_object):
#     # Create chore logic... (assuming you have logic to create the chore object)
#     notification = Notification.objects.create(
#         user=assigned_to,
#         message=f"You have been assigned a new chore: {chore_title}",
#         family=family,
#         chore=chore_object,  # Link the notification to the chore object
#     )
    
#     return notification
#     # Send notification email or implement chosen notification method here (To do)