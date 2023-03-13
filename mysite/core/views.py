from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.http import HttpResponse
from .forms import *
from .models import User, Employer, Employee, Asset, AssignedAsset

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


# employer profile
def employer_profile(request):
    user = request.user
    form = EmployerProfileForm(request.POST or None, instance=user, initial={
        'company_name': user.employer.company,
        'number_of_employees': user.employer.number_of_employees
    })

    if request.method == 'POST':
        if form.is_valid():
            user = form.save()
            messages.success(request, "Profile has been updated successfully")
            return redirect('core:employer_profile')

    return render(request, 'core/employer/profile.html', {'form': form})


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
    employee_position_edit_form = EmployeePositionChangeForm()
    return render(request, 'core/employer/employees.html', {
        'employees': employees,
        'employee_creation_form': emp_creation_form,
        'employee_position_edit_form': employee_position_edit_form
    })

def employer_assets(request):
    user = request.user
    employer_assets = Asset.objects.filter(employer=user.employer)
    all_assigned_assets = AssignedAsset.objects.all() # not effective
    assets = [] # build a list of tuples, (asset, employee_assigned_to or None)
    l = [a.asset for a in all_assigned_assets]
    for asset in employer_assets:
        try:
            i = l.index(asset) # if asset is assigned, get it index in l
            assets.append((asset, all_assigned_assets[i].employee))
        except ValueError:
            assets.append((asset, None))

    new_asset_form = AssetCreationForm()
    asset_assign_form = AssignAssetForm()
    asset_reclaim_form = ReclaimAssetForm()

    return render(request, 'core/employer/assets.html', {
        'assets': assets,
        'assigned_assets': l,
        'new_asset_form': new_asset_form,
        'asset_assign_form': asset_assign_form,
        'asset_reclaim_form': asset_reclaim_form
    })

def employer_notifications(request):
    return render(request, 'core/employer/notifications.html')
def employee_add(request):
    if request.method == 'POST':
        form = EmployeeCreationForm(request.POST)
        if form.is_valid():
            employee = form.save()
            Employee.objects.create(
                user = employee,
                employer = request.user.employer
            )
            messages.success(request, 'Employee has been added successfully')
            return redirect('core:employee_add')
    else:
        form = EmployeeCreationForm()

    return render(request, 'core/employer/employee_add.html', {'employee_creation_form': form})

def employee_position_edit(request):
    if request.method == 'POST':
        email = request.POST['email']
        employee = User.objects.get(email=email)
        form = EmployeePositionChangeForm(request.POST, instance=employee)
        if form.is_valid():
            # new_position = form.cleaned_data.get('position')
            employee = form.save()

            messages.success(request, 'Employee {} position changed to {}'.format(
                                employee.email,
                                employee.position
                            ))
            return redirect('core:employee_position_edit')
    else:
        form = EmployeePositionChangeForm()

    return render(request, 'core/employer/employee_position_edit.html', {'employee_position_edit_form': form})

# add company asset
def asset_add(request):
    if request.method == 'POST':
        form = AssetCreationForm(request.POST)
        if form.is_valid():
            # set the owner/employer before save
            form.set_employer(request.user.employer)
            asset = form.save()

            messages.success(request, 'Asset ' + asset.asset + ' added successfully.')
            return redirect('core:asset_add')
    else: # GET
        form = AssetCreationForm()
    return render(request, 'core/employer/asset_add.html', {'new_asset_form': form})


# display employee assigned asset
def employee_assigned_assets(request):
    assigned_assets = AssignedAsset.objects.filter(employee=request.user.employee)
    assets = [a.asset for a in assigned_assets]

    return render(request, 'core/employee/assigned_assets.html', {'assets': assets})


# employee profile
def employee_profile(request):
    form = EmployeeProfileForm(request.POST or None, instance=request.user)

    if request.method == 'POST':
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Your profile has been updated.')
    return render(request, 'core/employee/profile.html', {'form': form})

# assign an asset to an employee
def asset_assign(request):
    if request.method == 'POST':
        form = AssignAssetForm(request.POST)
        if form.is_valid():
            asset_id = form.cleaned_data.get('asset_id')
            employee_email = form.cleaned_data.get('employee_email')

            asset = AssignedAsset.objects.create(
                asset = Asset.objects.get(asset=asset_id),
                employee = User.objects.get(email=employee_email).employee
            )

            messages.success(request,
                'Asset ' + asset.asset.asset + ' has been assigned to '+ asset.employee.user.email)
            return redirect('core:asset_assign') # for assigning another asset
    else:
        form = AssignAssetForm()

    return render(request, 'core/employer/asset_assign.html', {'asset_assign_form': form})

# reclaim an assigned asset
def asset_reclaim(request):
    if request.method == 'POST':
        form = ReclaimAssetForm(request.POST)
        if form.is_valid():
            asset_id = form.cleaned_data.get('asset_id')
            assigned_asset = AssignedAsset.objects.get(asset_id=asset_id)
            assigned_asset.delete()
            messages.success(request,
                'Asset' + assigned_asset.asset.asset + ' has been re-claimed from '+ assigned_asset.employee.user.email)
            return redirect('core:asset_reclaim') # for reclaiming another asset
    else:
        form = ReclaimAssetForm()
    return render(request, 'core/employer/asset_reclaim.html', {'asset_reclaim_form': form})