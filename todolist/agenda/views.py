from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from .forms import CreateUserForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required(login_url='login')
def home(request):
    if request.method == 'POST':
        old_tasks = list(request.POST.get("tasks")[2:-1])
        tasks = []
        i = old_tasks[1:].index("'")
        while i < len(old_tasks):
            task = ''.join(old_tasks[:i+1])
            tasks.append(task)
            old_tasks = old_tasks[i+5:]
            if "'" in old_tasks:
                i = old_tasks[1:].index("'")
            else:
                break
        task = request.POST.get("task")
        if task not in tasks and len(tasks) > 0:
            tasks.append(task)
    else:
        tasks = ["task","other"]
    return render(request,'agenda/home.html', {
        "tasks":tasks,
        "username":request.user
    })



def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password =  request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request,"Username or password is incorrect.")
    
    return render(request, 'agenda\login.html')

def logoutUser(request):
    logout(request)
    return redirect('login')

def create_account(request):
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        print(form)
        if form.is_valid():
            form.save()
        else:
            messages.error(request, "Choose another username.")      
    return render(request, 'agenda/register.html', {
        "form":CreateUserForm()
    })