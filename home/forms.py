from typing import Any
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group
from django.contrib.auth import get_user_model
from django import forms
from .models import Member, Family, Chore, Budget, Expense, MonthlyBudget

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

class MemberCreationForm(forms.ModelForm):
    phone = forms.CharField(max_length=150, required=True)
    profile_pic = forms.ImageField()
    cover_pic = forms.ImageField()
    role = forms.ModelChoiceField(queryset=Group.objects.all())
    name = forms.CharField(max_length=255, required=True)
    email = forms.EmailField(max_length=200, required=True)

    class Meta:
        model = User
        fields = ['name', 'email', 'phone', 'role', 'profile_pic', 'cover_pic']
        exclude = ('password1', 'password2', )

    def __init__(self, *args: Any, family=None, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.family = family
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})

    def save(self, commit=True):
        user = User()
        username = generate_unique_username_from_str(self.cleaned_data['name'])
        user.username = username
        user.email = self.cleaned_data['email']  # Set the email on the User instance
        user.set_password(username)
        user.save()
        user.groups.add(self.cleaned_data['role'])
        role = 'FL' if self.cleaned_data['role'].name == 'Family Leader' else 'FM'
        member = Member.objects.create(
            user=user,
            name=self.cleaned_data['name'],
            email=self.cleaned_data['email'],
            phone=self.cleaned_data['phone'],
            profile_pic=self.cleaned_data['profile_pic'],
            cover_pic=self.cleaned_data['cover_pic'],
            role = role,
            family=self.family
        )
        if commit:
            member.save()
        return user
        
class FamilyCreationForm(forms.ModelForm):
    class Meta:
        model = Family
        fields = ['name', 'profile_pic']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['profile_pic'].widget.attrs.update({'required': True})
        
        
        
class ChoreCreationForm(forms.ModelForm):
    class Meta:
        model = Chore
        fields = ['title', 'description', 'assigned_to']

class MonthlyBudgetCreationForm(forms.ModelForm):
    class Meta:
        model = MonthlyBudget
        fields = ['amount', 'month', 'year']
        
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})

class BudgetCreationForm(forms.ModelForm):
    class Meta:
        model = Budget
        fields = ['amount', 'category', 'monthly_budget', 'year']

    def __init__(self, *args, **kwargs):
        self.family = kwargs.pop('family', None)
        super(BudgetCreationForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})
        if self.family is not None:
            self.fields['monthly_budget'].queryset = MonthlyBudget.objects.filter(family=self.family)

class ExpenseCreationForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['amount', 'description', 'month', 'year', 'category']
        
        def __init__(self, *args: Any, **kwargs: Any) -> None:
            super().__init__(*args, **kwargs)
            for field_name, field in self.fields.items():
                field.widget.attrs.update({'class': 'form-control'})
            self.fields['category'].widget.attrs['disabled'] = True

        def clean_category(self):
            # Use the initial value of the category field, because the disabled field value is not submitted
            return self.initial['category']