from django.contrib import admin
from .models import Family, Member, Chore, Expense, Budget, Notification
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User



def generate_unique_username_from_str(name):
    # Create the initial username
    name = name.replace(' ', '_')
    username = f"{name}".lower()
    # Ensure the username is unique
    User = get_user_model()
    counter = 0
    while User.objects.filter(username=username).exists():
        counter += 1
        username = f"{name}_{counter}".lower()
    return username

class MemberAdmin(admin.ModelAdmin):
    exclude = ('user', 'family')
    def save_model(self, request, obj, form, change):
        if not obj.user:  # if the teacher is being created for the first time
            # Create a new user
            username = generate_unique_username_from_str(obj.name)  
            password = username
            user = User.objects.create_user(username=username, password=password)
            obj.user = user
        obj.save()
        
       
admin.site.register(Member, MemberAdmin)    
admin.site.register(Family)
admin.site.register(Chore)
admin.site.register(Expense)
admin.site.register(Budget)
admin.site.register(Notification)
