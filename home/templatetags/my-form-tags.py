# myapp/templatetags/add_budget_tag.py
from django import template
from home.forms import MonthlyBudgetCreationForm, BudgetCreationForm, ExpenseCreationForm

register = template.Library()

@register.inclusion_tag('pages/add_monthly_budget.html', name='monthly_budget_form')
def monthly_budget_form(username):
    form = MonthlyBudgetCreationForm()
    return {'form': form, 'username': username}

@register.inclusion_tag('pages/add_budget.html', name='budget_form')
def budget_form(username):
    form = BudgetCreationForm()
    return {'form': form, 'username': username}

@register.inclusion_tag('pages/add_expense.html', name='expense_form')
def expense_form(username):
    form = ExpenseCreationForm()
    return {'form': form, 'username': username}


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)