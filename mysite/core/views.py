from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from .models import User, Employer, Employee, Asset, AssignedAsset
from .forms import EmployerSignupForm, EmployeeCreationForm, AssetCreationForm

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
    emp_creation_form = EmployeeCreationForm()
    return render(request, 'core/employer/employees.html', {
        'employees': employees,
        'form': emp_creation_form
    })

def employer_assets(request):
    user = request.user
    assets = Asset.objects.filter(employer=user.employer)
    form = AssetCreationForm()

    return render(request, 'core/employer/assets.html', {
        'assets': assets,
        'form': form
    })

def employer_profile(request):
    return render(request, 'core/employer/profile.html')

def employer_notifications(request):
    return render(request, 'core/employer/notifications.html')
def employee_add(request):
    if request.method == 'POST':
        form = EmployeeCreationForm(request.POST)
        if form.is_valid():
            form.save()
            emp = form.add_employer(request.user.employer)
            # unbind form for adding another user
            form = EmployeeCreationForm()

            # return redirect('core:employer_dashboard')
    else:
        form = EmployeeCreationForm()

    return render(request, 'core/employer/employee_add.html', {'form': form})

# add company asset
def asset_add(request):
    if request.method == 'POST':
        form = AssetCreationForm(request.POST)
        if form.is_valid():
            # set the owner/employer before save
            form.set_employer(request.user.employer)
            form.save()

            # unbind form for adding another asset
            form = AssetCreationForm()
    else: # GET
        form = AssetCreationForm()
    return render(request, 'core/employer/asset_add.html', {'form': form})
