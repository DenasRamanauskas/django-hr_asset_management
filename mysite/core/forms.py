from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from .models import (User, Employer, Employee, Asset, AssignedAsset)


class EmployerSignupForm(UserCreationForm):
    company_name = forms.CharField()
    CHOICES = (
        ('', 'Choose'),
        ('10', '10 Employees'),
        ('50', '50 Employees'),
        ('100', '100 Employees'),
        ('1000', '1000 Employees'),
    )
    number_of_employees = forms.ChoiceField(choices=CHOICES)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'phone_number', 'password1', 'password2')

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_employer = True
        user.save()

        company = self.cleaned_data.get('company_name')
        no_of_emp = self.cleaned_data.get('number_of_employees')
        employer = Employer.objects.create(
            user=user,
            company=company,
            number_of_employees=no_of_emp
        )
        return user


class EmployerProfileForm(forms.ModelForm):
    company_name = forms.CharField()
    CHOICES = (
        ('', 'Choose...'),
        ('10', '10 Employees'),
        ('50', '50 Employees'),
        ('100', '100 Employees'),
        ('1000', '1000 Employees'),
    )
    number_of_employees = forms.ChoiceField(choices=CHOICES)

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'phone_number',
        )

    def save(self):
        user = super().save()
        user.employer.company = self.cleaned_data.get('company_name')
        user.employer.number_of_employees = self.cleaned_data.get('number_of_employees')
        user.employer.save()

        return user


class EmployeeCreationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'position']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_employee = True
        user.save()

    @transaction.atomic
    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_employee = True
        user.save()

        return user


class EmployeePositionChangeForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'position']


class EmployeeProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'phone_number',
        )


class AssetCreationForm(forms.ModelForm):
    class Meta:
        model = Asset
        fields = ['asset', 'description']

    def set_employer(self, employer):
        self.employer = employer

    @transaction.atomic
    def save(self, commit=True):
        asset = super().save(commit=False)
        asset.employer = self.employer
        asset.save()

        return asset


class AssignAssetForm(forms.Form):
    asset_id = forms.CharField()
    employee_email = forms.EmailField()


class ReclaimAssetForm(forms.Form):
    asset_id = forms.CharField()
