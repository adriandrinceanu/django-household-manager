from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib import messages
from django.db.models import Sum
from datetime import datetime
from .models import Chore, Family, Member, Notification, Budget, MonthlyBudget, Expense
from django.contrib.auth.models import Group, User
from .utils import create_chore  # Import the create_chore function
from .forms import MemberCreationForm, FamilyCreationForm, ChoreCreationForm, BudgetCreationForm, MonthlyBudgetCreationForm, ExpenseCreationForm

def index(request):
    if request.user.is_authenticated:
        return render(request, 'pages/home.html')
    else:    
        return redirect('login')


def logoutPage(request):
    logout(request)
    return redirect('login')
 
def loginPage(request):
    if request.user.is_authenticated:
        username = request.user.username
        if request.user.groups.filter(name='Family Leader').exists():
            return redirect('family_leader', username=username)
        elif request.user.groups.filter(name='Family Member').exists():
            return redirect('family_member', username=username)
        else:
            return HttpResponse('You are not part of this Family group.')
    else:
        if request.method == "POST":
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                if user.groups.filter(name='Family Leader').exists():
                    return redirect('family_leader', username=username)
                elif user.groups.filter(name='Family Member').exists():
                    return redirect('family_member', username=username)
                else:
                    return HttpResponse('You are not part of this Family group.')
        groups = Group.objects.prefetch_related('user_set')    
        context = {'groups': groups}
        return render(request, 'accounts/login.html', context)
    
    
def registerPage(request):
    if request.method == 'POST':
        form = MemberCreationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = MemberCreationForm()
        
    context={
        'form':form,
    }
    return render(request,'accounts/register.html',context)

### family leader

@login_required
def create_chore_view(request, username):
    user = get_object_or_404(User, username=username)
    # Get the current user's family
    member = Member.objects.get(user=user)
    family = member.family

    # Get the family members and chores
    family_members = Member.objects.filter(family=family)
    chores = Chore.objects.filter(assigned_to__in=family_members)

    if request.method == 'POST':
        form = ChoreCreationForm(request.POST)
        if form.is_valid():
            chore = form.save(commit=False)
            if chore.assigned_to.family != family:
                messages.error(request, 'You can only assign chores to your family members.')
            else:
                chore.created_by = request.user  # Set the created_by field to the current user
                chore.save()
                messages.success(request, 'Chore created successfully.')
                return redirect('create_chore', username=username)
    else:
        # Only allow assigning chores to the user's family members
        form = ChoreCreationForm()
        form.fields['assigned_to'].queryset = family_members
    notifications = Notification.objects.filter(user=request.user)
    
    context = {
        'notifications': notifications,
        'chores': chores,
        'form': form,
        'segment': 'create_chore'
    }
    return render(request, 'pages/profile_leader_create_chore.html', context)


@login_required
def delete_chore_view(request, chore_id, username):
    user = get_object_or_404(User, username=username)
    # Get the chore object
    chore = get_object_or_404(Chore, id=chore_id)
    chore.delete()
    messages.success(request, 'Chore deleted successfully.')
    return redirect('create_chore',username=username)


@login_required
def familyLeader(request, username):
    user = get_object_or_404(User, username=username)
    member = Member.objects.get(user=user)
    family_members = Member.objects.filter(family=member.family)
    
    context = {
        'member': member,
        'family': family_members,
        'segment': 'family_leader',
        
    }
    
    return render(request, 'pages/profile_leader.html', context)


@login_required
def create_family(request, username):
    user = get_object_or_404(User, username=username)
    member = Member.objects.get(user=user)
    if member.role != 'FL':
        messages.error(request, 'Only a Family Leader can create new members.')
        return redirect('/')
    
    my_family = member.family
    family_members = Member.objects.filter(family=member.family)
    family_form = FamilyCreationForm()
    member_form = MemberCreationForm()

    if request.method == 'POST':
        if 'create_family' in request.POST:
            family_form = FamilyCreationForm(request.POST, request.FILES)
            if family_form.is_valid():
                family = family_form.save(commit=False)  # Don't save the form to the database yet
                family.created_by = request.user  # Set the created_by field to the current user
                family.save()  # Now you can save it to the database
                member.family = family  # Add the member to the newly created family
                member.save()  # Save the updated member object
                my_family = member.family
                messages.success(request, 'Family created successfully')
                return redirect('create_family', username=username)  
        elif 'create_member' in request.POST:
            member_form = MemberCreationForm(request.POST, request.FILES, family=my_family)
            if member_form.is_valid():
                new_member = member_form.save(commit=False)  # Don't save the form to the database yet
                new_member.family = my_family  # Set the family of the new member
                new_member.save()  # Now you can save it to the database
                family_members = Member.objects.filter(family=my_family)  # Update the family_members variable
                messages.success(request, 'Member created successfully')
                return redirect('create_family', username=username)  

    context = {
        'member': member,
        'my_family': my_family,
        'family': family_members,
        'family_form': family_form,
        'member_form': member_form,
        'segment': 'create_family',
    }
    return render(request, 'pages/profile_leader_family_creation.html', context)

### end family leader


### start budget logic
@login_required
def budget_view(request, username):
    user = get_object_or_404(User, username=username)
    member = Member.objects.get(user=user)

    # Get all monthly budgets for the current user's family
    monthly_budgets = MonthlyBudget.objects.filter(family=member.family)
    
    
    # Get the months from the model
    months = [month[0] for month in MonthlyBudget.MONTH_CHOICES]

    # Create a dictionary where the keys are the months and the values are the budgets
    monthly_budget_dict = {month: 0 for month in months}  # Initialize the dictionary with 0 for each month

    for budget in monthly_budgets:
        monthly_budget_dict[budget.month] = budget.amount
        
    # Prepare data for each monthly budget
    monthly_budget_data = []
    yearly_budget = 0
    for monthly_budget in monthly_budgets:
        # Get all budgets associated with the current monthly budget
        budgets = Budget.objects.filter(monthly_budget=monthly_budget)

        # Calculate the total budget and the remaining amount
        total_budget = sum(budget.amount for budget in budgets)
        remaining_amount = monthly_budget.amount - total_budget

        # Add the initial amount to the yearly budget
        yearly_budget += monthly_budget.amount

        monthly_budget_data.append({
            'monthly_budget': monthly_budget,
            'budgets': budgets,
            'total_budget': total_budget,
            'remaining_amount': remaining_amount,
        })

    # Render the budgets view
    if request.user.groups.filter(name='Family Leader').exists():
        return render(request, 'pages/profile_leader_create_budget.html', \
            {'monthly_budget_data': monthly_budget_data, 'yearly_budget': yearly_budget, 'months': months, \
                'monthly_budget_dict': monthly_budget_dict, 'segment': 'budgets',})
    else:
        return render(request, 'pages/profile_member_view_budget.html', \
            {'monthly_budget_data': monthly_budget_data, 'yearly_budget': yearly_budget, 'months': months, \
                'monthly_budget_dict': monthly_budget_dict, 'segment': 'view_budgets',})


@login_required
def add_monthly_budget(request, username):
    user = get_object_or_404(User, username=username)
    member = Member.objects.get(user=user)
    if request.method == 'POST':
        form = MonthlyBudgetCreationForm(request.POST)
        if form.is_valid():
            monthly_budget = form.save(commit=False)
            monthly_budget.family = member.family  # Associate the budget with the user's family
            monthly_budget.save()
            return redirect('budgets', username=username)
    else:
        form = MonthlyBudgetCreationForm()
    return render(request, 'pages/add_monthly_budget.html', {'form': form,'username': username})

@login_required
def add_budget(request, username):
    user = get_object_or_404(User, username=username)
    member = Member.objects.get(user=user)
    if request.method == 'POST':
        form = BudgetCreationForm(request.POST)
        if form.is_valid():
            budget = form.save(commit=False)
            budget.monthly_budget.family = member.family  # Associate the budget with the user's family
            budget.save()
            return redirect('budgets', username=username)
    else:
        form = BudgetCreationForm()
    return render(request, 'pages/add_budget.html', {'form': form, 'username': username})


@login_required
def delete_monthly_budget(request, username, budget_id):
    user = get_object_or_404(User, username=username)
    member = Member.objects.get(user=user)
    monthly_budget = get_object_or_404(MonthlyBudget, id=budget_id, family=member.family)
    monthly_budget.delete()
    return redirect('budgets', username=username)

@login_required
def delete_budget(request, username, budget_id):
    user = get_object_or_404(User, username=username)
    member = Member.objects.get(user=user)
    budget = get_object_or_404(Budget, id=budget_id, monthly_budget__family=member.family)
    budget.delete()
    return redirect('budgets', username=username)

### end budget logic


### start expense logic

@login_required
def expense_view(request, username):
    user = get_object_or_404(User, username=username)
    member = Member.objects.get(user=user)

    current_month = datetime.now().strftime('%b').lower()
    current_year = datetime.now().year

    # Get all monthly budgets for the current user's family for the current month
    monthly_budgets = MonthlyBudget.objects.filter(family=member.family, month=current_month, year=current_year)

    # Prepare data for each monthly budget
    monthly_budget_data = []
    for monthly_budget in monthly_budgets:
        # Get all budgets associated with the current monthly budget
        budgets = Budget.objects.filter(monthly_budget=monthly_budget)

        # Prepare data for each budget
        budget_data = []
        for budget in budgets:
            # Get all expenses associated with the current budget
            expenses = Expense.objects.filter(budget=budget)

            # Calculate the total expense and the remaining amount
            total_expense = expenses.aggregate(Sum('amount'))['amount__sum'] or 0
            if total_expense is not None:
                remaining_amount = budget.amount - total_expense
            else:
                remaining_amount = budget.amount
                
            # Get the members who created the expenses
            spenders = set(expense.created_by.all() for expense in expenses)

            budget_data.append({
                'budget': budget,
                'expenses': expenses,
                'total_expense': total_expense,
                'remaining_amount': remaining_amount,
                'spenders': spenders,
            })

        monthly_budget_data.append({
            'monthly_budget': monthly_budget,
            'budgets': budget_data,
        })

    # Calculate the total expense for each category
    category_expenses = {}
    for category, _ in Expense.CATEGORY_CHOICES:
        total_expense = Expense.objects.filter(category=category, month=current_month, year=current_year).aggregate(Sum('amount'))['amount__sum'] or 0
        category_expenses[category] = total_expense
        
    # Get the budget for each category for the current month and calculate the remaining budget
    remaining_category_budgets = {}
    for category, _ in Expense.CATEGORY_CHOICES:
        category_budget = Budget.objects.filter(monthly_budget__family=member.family, monthly_budget__month=current_month, monthly_budget__year=current_year, category=category).first()
        total_category_expenses = Expense.objects.filter(created_by=member, month=current_month, year=current_year, category=category).aggregate(Sum('amount'))['amount__sum'] or 0

        if category_budget and total_category_expenses:
            remaining_category_budgets[category] = category_budget.amount - total_category_expenses
        elif category_budget:
            remaining_category_budgets[category] = category_budget.amount
        else:
            remaining_category_budgets[category] = 0

        
     # Get the budget for each category for the current month
    category_budgets = {}
    for category, _ in Expense.CATEGORY_CHOICES:
        category_budget = Budget.objects.filter(monthly_budget__family=member.family, monthly_budget__month=current_month, monthly_budget__year=current_year, category=category).first()
        category_budgets[category] = category_budget
        
    #  # Get the expenses for each category for the current month and group them by the created_by field
    # category_expenses_by_member = {}
    # for category, _ in Expense.CATEGORY_CHOICES:
    #     expenses_by_member = Expense.objects.filter(created_by__family=member.family, month=current_month, year=current_year, category=category).values('created_by__name', 'created_by__profile_pic').annotate(total_expense=Sum('amount'))
    #     category_expenses_by_member[category] = list(expenses_by_member)
            
    # Get all expenses and budgets per year
    yearly_expenses = Expense.objects.filter(created_by=member).order_by('-year')
    yearly_budgets = Budget.objects.filter(monthly_budget__family=member.family).order_by('-year')
    
    # Create a list of dictionaries where each dictionary contains the month, budget, and expenses FOR THE CHART
    months = [month[0] for month in Expense.MONTH_CHOICES]
    # Create a dictionary where the keys are the months and the values are the budgets
    monthly_budget_dict = {budget.month: budget for budget in monthly_budgets}
    monthly_data = []
    for month in months:
        budget = monthly_budget_dict.get(month)
        expenses = category_expenses.get(month, 0)
        monthly_data.append({'month': month, 'budget': budget, 'expenses': expenses})
           
    # Prepare data for the chart lines
    chart_data = []
    for month in months:
        # Get the monthly budget for the current month, or None if it doesn't exist
        monthly_budget = MonthlyBudget.objects.filter(family=member.family, month=month, year=current_year).first()

        # Calculate the total expense for the current month
        total_expense = Expense.objects.filter(created_by__family=member.family, month=month, year=current_year).aggregate(Sum('amount'))['amount__sum'] or 0

        # If a monthly budget exists for the current month, use its amount, otherwise use 0
        budget = monthly_budget.amount if monthly_budget else 0

        chart_data.append({
            'month': month,
            'budget': budget,
            'expenses': total_expense,
        })

    table_data = []
    for category, _ in Expense.CATEGORY_CHOICES:
        budget = category_budgets.get(category)
        expenses = category_expenses.get(category, 0)
        remaining = remaining_category_budgets.get(category, '0')
        spenders = Expense.objects.filter(category=category, created_by__family=member.family)
        table_data.append({
            'category': category,
            'budget': budget.amount if budget else '0',
            'expenses': expenses,
            'remaining': remaining,
            'spenders': spenders,
    })
        
    expenses = Expense.objects.filter(created_by__family=member.family).order_by('-created_at')
    expense_data = []
    for expense in expenses:
        spenders = ", ".join([spender.name for spender in expense.created_by.all()])
        expense_data.append({
            'id': expense.id,
            'amount': expense.amount,
            'category': expense.get_category_display(),
            'description': expense.description,
            'spenders': spenders,
        })
    
    # Calculate the total expenses for the current month
    total_expenses_current_month = Expense.objects.filter(created_by__family=member.family, month=current_month, year=current_year).aggregate(Sum('amount'))['amount__sum'] or 0
    context = {
        
        'monthly_budget_data': monthly_budget_data,
        'category_expenses': category_expenses, 
        'current_month': current_month, 
        'yearly_expenses': yearly_expenses,
        'yearly_budgets': yearly_budgets, 
        'category_budgets': category_budgets, 
        'remaining_category_budgets': remaining_category_budgets,
        'monthly_budget_dict': monthly_budget_dict, 
        'monthly_data': monthly_data,
        'chart_data': chart_data, 
        'table_data': table_data, 
        'expense_data': expense_data,
        'total_expenses_current_month': total_expenses_current_month,
        'segment': 'expenses',
                    }
    # Render the expenses view
    if request.user.groups.filter(name='Family Leader').exists():
        return render(request, 'pages/profile_leader_expenses.html', context)
    else:
        return render(request, 'pages/profile_member_expenses.html', context)



@login_required
def add_expense(request, username):
    user = get_object_or_404(User, username=username)
    member = Member.objects.get(user=user)
    if request.method == 'POST':
        form = ExpenseCreationForm(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.save()  # Save the expense instance to the database
            expense.created_by.add(member)  # Now you can add the member to the created_by field
            return redirect('expenses', username=username)
    else:
        form = ExpenseCreationForm()
    return render(request, 'pages/add_expense.html', {'form': form})



@login_required
def delete_expense(request, username, expense_id):
    user = get_object_or_404(User, username=username)
    member = Member.objects.get(user=user)
    # Get the Expense object
    expense = get_object_or_404(Expense, id=expense_id)
    # Check if the current user is one of the creators of the expense
    if request.user.member in expense.created_by.all():
        # If so, delete the expense
        expense.delete()
    return redirect('expenses',username=username)


### end expense logic

### Family Member logic 

@login_required
def familyMember(request, username):
    user = get_object_or_404(User, username=username)
    member = Member.objects.get(user=user)
    family_members = Member.objects.filter(family=member.family)
    my_family = member.family

    # Get the current month and year
    current_month = datetime.now().strftime('%b').lower()
    current_year = datetime.now().year

    # Get the budgets for the current month
    monthly_budgets = MonthlyBudget.objects.filter(family=my_family, month=current_month, year=current_year)
    budgets = Budget.objects.filter(monthly_budget__in=monthly_budgets)

    context = {
        'member': member,
        'family': family_members,
        'my_family': my_family,
        'budgets': budgets,  # Add budgets to the context
        'current_month': current_month,
        'segment': 'family_member',
    }
    
    return render(request, 'pages/profile_member.html', context)


@login_required
def chore_view(request, username):
    user = get_object_or_404(User, username=username)
    # Get the current user's member instance
    member = Member.objects.get(user=user)
    # Get the chores assigned to the user
    chores = Chore.objects.filter(assigned_to=member)
    context = {
        'chores': chores,
        'segment': 'chore_view'
    }
    return render(request, 'pages/profile_member_chore_view.html', context)

@login_required
def chore_done(request, chore_id):
    # Get the Member object for the current user
    member = get_object_or_404(Member, user=request.user)

    # Get the Chore object for the given id that is assigned to the current member
    chore = get_object_or_404(Chore, id=chore_id, assigned_to=member)

    # Mark the chore as done
    chore.is_done = True
    chore.save()

    return redirect('chore_view', username=request.user.username)