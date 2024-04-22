from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone



class Family(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True)
    created_by = models.ForeignKey(User, related_name='families', on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to='profile_pic', null=True, blank=True)
    
    def __str__(self):
        return self.name

class Member(models.Model):
    ROLE_CHOICES = (
        ('FL', 'Family Leader'),
        ('FM', 'Family Member'),
    )
    
    user = models.OneToOneField(User, on_delete=models.CASCADE,null=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    email = models.CharField(max_length=200, null=True)
    phone = models.CharField(max_length=150, null=True)
    profile_pic = models.ImageField(upload_to='profile_pic',null=True, blank=True)
    cover_pic = models.ImageField(upload_to='cover_pic',null=True, blank=True)
    family = models.ForeignKey(Family, related_name='family_members', on_delete=models.CASCADE, null=True, blank=True)
    role = models.CharField(max_length=2, choices=ROLE_CHOICES, default='FM')
    created_by = models.ForeignKey(User, related_name='created_members', on_delete=models.CASCADE, null=True, blank=True)
    
    def __str__(self) -> str:
        return self.name
    

class Chore(models.Model):
    title = models.CharField(max_length=255)
    assigned_to = models.ForeignKey(Member, related_name='chores', on_delete=models.CASCADE)
    deadline = models.DateField()
    is_done = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, related_name='assigned_chores', on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.title} - Assigned to: {self.assigned_to.name}"

class Expense(models.Model):
    CURRENT_YEAR = timezone.now().year
    YEAR_CHOICES = [(r,r) for r in range(CURRENT_YEAR, CURRENT_YEAR+20)]
    CATEGORY_CHOICES = [
        ('groceries', 'Groceries'),
        ('entertainment', 'Entertainment'),
        ('clothing', 'Clothing'),
        ('transportation', 'Transportation'),
        ('utilities', 'Utilities'),
        ('healthcare', 'Healthcare'),
        ('education', 'Education'),
        ('other', 'Other'),
    ]
    
    MONTH_CHOICES = [
        ('jan', 'January'),
        ('feb', 'February'),
        ('mar', 'March'),
        ('apr', 'April'),
        ('may', 'May'),
        ('jun', 'June'),
        ('jul', 'July'),
        ('aug', 'August'),
        ('sep', 'September'),
        ('oct', 'October'),
        ('nov', 'November'),
        ('dec', 'December'),
    ]
    amount = models.DecimalField(max_digits=7, decimal_places=0)
    description = models.CharField(max_length=255)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    month = models.CharField(max_length=3, choices=MONTH_CHOICES,null=True, blank=True)
    year = models.PositiveIntegerField(choices=YEAR_CHOICES, default=CURRENT_YEAR, null=True, blank=True)
    created_by = models.ManyToManyField(Member, related_name='expenses')
    created_at = models.DateTimeField(auto_now_add=True)
    budget = models.ForeignKey('Budget', related_name='expense', on_delete=models.CASCADE, null=True, blank=True)
    is_read = models.BooleanField(default=False)
    
    def is_current_month(self):
        # Get the current date
        current_date = timezone.now().date()

        # Check if the current month is the same as the created_at field
        if self.created_at and self.created_at.month == current_date.month:
            return True
        else:
            return False
        
    def __str__(self):
        if self.created_by.exists():
            members = ", ".join([member.name for member in self.created_by.all()])
            return f"{self.amount} RON - {self.category} - {self.description} - Paid by: {members}"
        else:
            return f"{self.amount} RON - {self.category} - {self.description} - Paid by: Not Assigned" 

class MonthlyBudget(models.Model):
    CURRENT_YEAR = timezone.now().year
    YEAR_CHOICES = [(r,r) for r in range(CURRENT_YEAR, CURRENT_YEAR+20)]
    MONTH_CHOICES = [
        ('jan', 'January'),
        ('feb', 'February'),
        ('mar', 'March'),
        ('apr', 'April'),
        ('may', 'May'),
        ('jun', 'June'),
        ('jul', 'July'),
        ('aug', 'August'),
        ('sep', 'September'),
        ('oct', 'October'),
        ('nov', 'November'),
        ('dec', 'December'),
    ]
    amount = models.DecimalField(max_digits=7, decimal_places=0)
    month = models.CharField(max_length=3, choices=MONTH_CHOICES, null=True, blank=True)
    year = models.PositiveIntegerField(choices=YEAR_CHOICES, default=CURRENT_YEAR, null=True, blank=True)
    family = models.ForeignKey(Family, related_name='monthly_budgets', on_delete=models.CASCADE)
    
    
    
    def amount_in_ron(self):
        return f"{self.amount} RON"

    def __str__(self):
        return f"Monthly Budget: {self.amount} for {self.family.name} in {self.get_month_display()}"
    

class Budget(models.Model):
    CURRENT_YEAR = timezone.now().year
    YEAR_CHOICES = [(r,r) for r in range(CURRENT_YEAR, CURRENT_YEAR+20)]
    amount = models.DecimalField(max_digits=7, decimal_places=0)
    category = models.CharField(max_length=50, choices=Expense.CATEGORY_CHOICES)
    monthly_budget = models.ForeignKey(MonthlyBudget, related_name='budgets', on_delete=models.CASCADE, null=True, blank=True)
    year = models.PositiveIntegerField(choices=YEAR_CHOICES, default=CURRENT_YEAR, null=True, blank=True)
    
    def amount_in_ron(self):
        return f"{self.amount} RON"

    def __str__(self):
        return f"Budget: {self.amount} for category {self.category} in {self.monthly_budget}"
    
    
class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, related_name="notifications", null=True)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    family = models.ForeignKey(Family, on_delete=models.CASCADE, related_name="notifications", null=True)
    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name="member", null=True )
    chore = models.ForeignKey(Chore, on_delete=models.CASCADE, null=True, blank=True)  

    def __str__(self):
        return f"Notification for {self.family} family: {self.message}"
    
class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    family = models.ForeignKey(Family, on_delete=models.CASCADE, null=True, blank=True)
    username = models.CharField(max_length=255, null=True, blank=True)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    chat_id = models.CharField(max_length=255, null=True, blank=True)  

    def __str__(self):
        return self.user.username if self.user else 'Anonymous'
    
class UnreadMessage(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE, null=True, blank=True)
    message = models.ForeignKey(Message, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    is_read = models.BooleanField(default=False)
    
    
