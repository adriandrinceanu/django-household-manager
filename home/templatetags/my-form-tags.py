# myapp/templatetags/add_budget_tag.py
from django import template
from home.forms import MonthlyBudgetCreationForm, BudgetCreationForm, ExpenseCreationForm, MonthlyBudget
from home.models import Member, Budget
from django.contrib.auth.models import User
from django.db.models import Sum



register = template.Library()

@register.inclusion_tag('pages/add_monthly_budget.html', name='monthly_budget_form')
def monthly_budget_form(username):
    form = MonthlyBudgetCreationForm()
    return {'form': form, 'username': username}

@register.inclusion_tag('pages/add_budget.html', name='budget_form')
def budget_form(username):
    user = User.objects.get(username=username)
    member = Member.objects.get(user=user)
    family = member.family
    form = BudgetCreationForm(family=family)
    # Get the total budget for the month
    total_monthly_budget = MonthlyBudget.objects.filter(family=family).aggregate(Sum('amount'))['amount__sum'] or 0
    # Get the total allocated budget for the month
    total_allocated_budget = Budget.objects.filter(monthly_budget__family=family).aggregate(Sum('amount'))['amount__sum'] or 0
    # Calculate the remaining budget
    remaining_budget = total_monthly_budget - total_allocated_budget
    return {'form': form, 'username': username, 'remaining_budget': remaining_budget}

@register.inclusion_tag('pages/add_expense.html', name='expense_form')
def expense_form(username):
    form = ExpenseCreationForm()
    return {'form': form, 'username': username}


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

@register.filter(name="in_group")
def in_group(user, group_name):
    return user.groups.filter(name=group_name).exists()
