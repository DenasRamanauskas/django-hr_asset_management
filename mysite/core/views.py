from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from .models import User, Employer, Employee, Asset, AssignedAsset

from .forms import EmployerSignupForm

# Create your views here.
def home(request):
    return render(request, 'core/home.html')

def employer_signup(request):
    if request.method == 'POST':
        form = EmployerSignupForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            password1 = form.cleaned_data.get('password1')
            user = authenticate(request, email=email, password=password1)
            if user is not None:
                login(request, user)
                return redirect('core:employer_dashboard')
    else:
        form = EmployerSignupForm()
    return render(request, 'core/employer/signup.html', {'form': form})

def employer_dashboard(request):
    return render(request, 'core/employer/dashboard.html')

def employee_dashboard(request):
    return render(request, 'core/employee/dashboard.html')

def login_redirect(request):
    if request.user.is_employer:
        return redirect('core:employer_dashboard')
    return redirect('core:employee_dashboard')

def employees_list(request):
    user = request.user
    employees = Employee.objects.filter(employer=user.employer)
    employees = [e.user for e in employees]
    return render(request, 'core/employer/employees.html', {'employees': employees})

def employer_assets(request):
    user = request.user
    assets = Asset.objects.filter(employer=user.employer)
    return render(request, 'core/employer/assets.html', {'assets': assets})

def employer_profile(request):
    return render(request, 'core/employer/profile.html')

def employer_notifications(request):
    return render(request, 'core/employer/notifications.html')