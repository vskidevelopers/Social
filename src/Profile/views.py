from django.shortcuts import render
from .models import *

# Create your views here.
def profile_view(request):
    profile= Profiles.objects.get(user=request.user)
    context = {
        'profile':profile
    }
    return render(request, 'profile/profile.html', context )