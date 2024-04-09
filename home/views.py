from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .models import Chore, Family, Member, Notification, Budget, MonthlyBudget
from django.contrib.auth.models import Group, User
from .utils import create_chore  # Import the create_chore function
from .forms import MemberCreationForm, FamilyCreationForm, ChoreCreationForm, BudgetCreationForm, MonthlyBudgetCreationForm

def index(request):
    if request.user.is_authenticated:
        return render(request, 'pages/index.html')
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
        'member_form': member_form
    }
    return render(request, 'pages/profile_leader_family_creation.html', context)

### end family leader


### start budget logic

def budget_view(request, username):
    user = get_object_or_404(User, username=username)
    member = Member.objects.get(user=user)

    # Get all monthly budgets for the current user's family
    monthly_budgets = MonthlyBudget.objects.filter(family=member.family)

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
    return render(request, 'pages/profile_leader_create_budget.html', \
        {'monthly_budget_data': monthly_budget_data, 'yearly_budget': yearly_budget})


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
    return render(request, 'pages/add_monthly_budget.html', {'form': form})

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
    return render(request, 'pages/add_budget.html', {'form': form})





def edit_budget(request, pk):
    budget = Budget.objects.get(pk=pk)
    if request.method == 'POST':
        form = BudgetCreationForm(request.POST, instance=budget)
        if form.is_valid():
            form.save()
            return redirect('budgets')
    else:
        form = BudgetCreationForm(instance=budget)
    return render(request, 'edit_budget.html', {'form': form})

### end budget logic