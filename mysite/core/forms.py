from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from .models import (User, Employer, Employee, Asset, AssignedAsset)

# employer signup form
class EmployerSignupForm(UserCreationForm):
    company_name = forms.CharField()
    number_of_employees = forms.IntegerField()

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'phone_number', 'password1', 'password2')

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_employer = True
        user.save()

        # create employer profile for user
        company = self.cleaned_data.get('company_name')
        no_of_emp = self.cleaned_data.get('number_of_employees')
        employer = Employer.objects.create(
            user=user,
            company=company,
            number_of_employees=no_of_emp
        )
        return user


# employer view/update profile
class EmployerProfileForm(forms.ModelForm):
    company_name = forms.CharField()
    number_of_employees = forms.IntegerField()

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'phone_number',
        )

    def save(self):
        user = super().save()

        # update corresponding employer profile
        user.employer.company = self.cleaned_data.get('company_name')
        user.employer.number_of_employees = self.cleaned_data.get('number_of_employees')
        user.employer.save()

        return user

class EmployeeCreationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'position']

    # designate user as an employee
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

class AssetCreationForm(forms.ModelForm):

    class Meta:
        model = Asset
        fields = ['asset', 'description']

    # asset belongs to an employer
    def set_employer(self, employer):
        self.employer = employer

    @transaction.atomic
    def save(self, commit=True):
        asset = super().save(commit=False)
        asset.employer = self.employer # expects employer to have been set
        asset.save()

        return asset
