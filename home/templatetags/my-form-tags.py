# myapp/templatetags/add_budget_tag.py
from django import template
from home.forms import BudgetCreationForm

register = template.Library()

@register.inclusion_tag('pages/add_budget.html', name='budget_form')
def budget_form():
    form = BudgetCreationForm()
    return {'form': form}