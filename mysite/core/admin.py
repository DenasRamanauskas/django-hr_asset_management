from django.contrib import admin
from .models import (User, Employer, Employee, Asset, AssignedAsset)
from .forms import UserCreationForm

admin.site.register(User)
admin.site.register(Employer)
admin.site.register(Employee)
admin.site.register(Asset)
admin.site.register(AssignedAsset)