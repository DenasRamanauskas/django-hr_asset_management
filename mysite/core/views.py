from django.shortcuts import render

# Create your views here.
def home(request):
    '''
    handles requests to the home page.
    '''
    return render(request, 'core/home.html')