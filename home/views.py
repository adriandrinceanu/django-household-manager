from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .models import Chore, Family, Member
from django.contrib.auth.models import Group, User
from .utils import create_chore  # Import the create_chore function
from .forms import MemberCreationForm, FamilyCreationForm

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

   
def create_chore_view(request, family_id):
    # Your view logic to handle creating a chore...
    if request.method == 'POST':
        # Get form data
        title = request.POST['title']
        assigned_to = request.user  # Assuming you get the assigned user from the request
        family = Family.objects.get(pk=family_id)
        # Create the chore object (logic here)
        chore = Chore.objects.create(title=title, assigned_to=assigned_to, family=family)
        create_chore(assigned_to, title, family, chore)  # Call the create_chore function
        # Handle successful creation and potentially redirect
    return render(request, 'create_chore.html')

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
                my_family = member.family
                messages.success(request, 'Family created successfully')
                return redirect('create_family', username=username)  
        elif 'create_member' in request.POST:
            member_form = MemberCreationForm(request.POST, request.FILES)
            if member_form.is_valid():
                member = member_form.save(commit=False)
                member.save()
                member.family = my_family
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