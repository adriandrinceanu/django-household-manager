from django.db import models
from django.contrib.auth.models import User


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
    description = models.TextField(blank=True)
    assigned_to = models.ForeignKey(Member, related_name='chores', on_delete=models.CASCADE)
    is_done = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.title} - Assigned to: {self.assigned_to.name}"

class Expense(models.Model):
    CATEGORY_CHOICES = [
        ('food', 'Food'),
        ('clothing', 'Clothing'),
        ('movies', 'Movies'),
        ('transportation', 'Transportation'),
        ('groceries', 'Groceries'),
        ('snacks', 'Snacks'),
        ('sweets', 'Sweets'),
        ('utilities', 'Utilities'),
        ('healthcare', 'Healthcare'),
        ('entertainment', 'Entertainment'),
        ('education', 'Education'),
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
    amount = models.DecimalField(max_digits=7, decimal_places=2)
    description = models.CharField(max_length=255)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    month = models.CharField(max_length=3, choices=MONTH_CHOICES,null=True, blank=True)
    year = models.PositiveIntegerField(null=True, blank=True)
    created_by = models.ForeignKey(Member, related_name='expenses', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.amount} - {self.description} - Paid by: {self.created_by.username}"

class MonthlyBudget(models.Model):
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
    amount = models.DecimalField(max_digits=7, decimal_places=2)
    month = models.CharField(max_length=3, choices=MONTH_CHOICES, null=True, blank=True)
    year = models.PositiveIntegerField(null=True, blank=True)
    family = models.ForeignKey(Family, related_name='monthly_budgets', on_delete=models.CASCADE)
    
    def amount_in_ron(self):
        return f"{self.amount} RON"

    def __str__(self):
        return f"Monthly Budget: {self.amount} for {self.family.name} in {self.get_month_display()}"
    

class Budget(models.Model):
    amount = models.DecimalField(max_digits=7, decimal_places=2)
    category = models.CharField(max_length=50, choices=Expense.CATEGORY_CHOICES)
    monthly_budget = models.ForeignKey(MonthlyBudget, related_name='budgets', on_delete=models.CASCADE, null=True, blank=True)
    
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
    chore = models.ForeignKey(Chore, on_delete=models.CASCADE, null=True, blank=True)  # Optional field for chore notifications

    def __str__(self):
        return f"Notification for {self.user.username}: {self.message}"
    
    
