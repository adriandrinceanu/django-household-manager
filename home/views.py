from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.contrib.auth import login,logout,authenticate
from .models import Chore, Family, Member
from django.contrib.auth.models import Group, User
from .utils import create_chore  # Import the create_chore function
from .forms import MemberCreationForm

def index(request):

    # Page from the theme 
    return render(request, 'pages/index.html')


def homepage(request):
    return render(request, 'home.html')

def logoutPage(request):
    logout(request)
    return redirect('/')
 
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
        return render(request, 'login.html', context)
    
    
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
    return render(request,'register.html',context)

   
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

def familyLeader(request, username):
    user = get_object_or_404(User, username=username)
    member = Member.objects.get(user=user)
    family_members = Member.objects.filter(family=member.family)
    
    context = {
        'member': member,
        'family': family_members,
    }
    
    return render(request, 'family_leader.html', context)