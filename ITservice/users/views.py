from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .form import RegisterCustomerForm


# Create your views here.
def register_customer(request):
    if request.method == 'POST':
        form = RegisterCustomerForm(request.POST)
        if form.is_valid():
            var = form.save(commit=False)
            var.is_customer = True
            var.save()
            messages.info(request, 'Your account has been successfully registered. Please login to continue')
            return redirect('login')
        else:
            messages.warning(request, 'Something were wrong. Please check form inputs')
            return redirect('register-customer')
    else:
        form = RegisterCustomerForm()
        context = {'form':form}
        return render(request, 'users/register_customer.html', context)
    
#User login
def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user =  authenticate(request, username=username, password=password)
        if user is not None and user.is_active:
            login(request, user)
            messages.info(request, 'Login successfull')
            return redirect('dashboard')
        else:
            messages.warning(request, 'Something were wrong. Please check form input')
            return redirect('login')
    else:
        return render(request, 'users/login.html')
    
#User logout
def logout_user(request):
    logout(request)
    messages.info(request, 'Your session has ended')
    return redirect('login')