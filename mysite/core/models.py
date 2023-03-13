from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    username = models.CharField(max_length=200, blank=False)
    email = models.EmailField(max_length=200, unique=True, blank=False)
    is_employer = models.BooleanField(default=False)
    is_employee = models.BooleanField(default=False)
    position = models.CharField(default=None, max_length=200)
    phone_number = models.CharField(default=None, max_length=15, blank=False)
    date_of_birth = models.DateField(default=None, blank=True, null=True)

    REQUIRED_FIELDS = ['username',]

    USERNAME_FIELD = 'email'

class Employer(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True
    )

    company = models.CharField(max_length=200)

    number_of_employees = models.IntegerField(default=0)


class Employee(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True
    )

    employer = models.ForeignKey(Employer, on_delete=models.CASCADE)