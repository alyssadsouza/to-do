from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from .forms import CreateUserForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required(login_url='login')
def home(request):
    return render(request,'agenda/home.html', {
        "tasks":['Wash Dishes', 'Fold Laundry']
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