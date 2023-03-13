from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.http import HttpResponse

from .forms import EmployerSignupForm

# Create your views here.
def home(request):
    '''
    handles requests to the home page.
    '''
    return render(request, 'core/home.html')