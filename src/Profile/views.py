from django.shortcuts import render
from .models import *
from .forms import ProfileModelForm
from django.views.generic import ListView

# Create your views here.
def profile_view(request):
    profile= Profiles.objects.get(user=request.user)
    form =  ProfileModelForm(request.POST or None,request.FILES or None, instance=profile )
    confirm=False

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            confirm=True

    context = {
        'profile':profile,
        'form':form,
        'confirm':confirm
    }
    return render(request, 'profile/profile.html', context )

def requests_view(request):
    profile=Profiles.objects.get(user=request.user)    
    invites=Friendship.objects.friend_requests_recieved(profile)

    context={
        "invites":invites
    }

    return render(request, 'profile/invites.html', context)

def profile_list_view(request):
    user=request.user
    profiles=Profiles.objects.get_profiles(user=user)

    context ={
        'profiles':profiles
    }
    return render(request, 'profile/profiles.html', context)


class ProfilesListView(ListView):
    model = Profiles
    template_name = "profile/profiles.html"


def profiles_available_for_invites(request):
    sender=request.user
    profiles=Profiles.objects.get_profiles_available_for_invite(sender=sender)

    context ={
        'profiles':profiles
    }
    return render(request, 'profile/availables.html', context)