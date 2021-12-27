from django.shortcuts import get_object_or_404, redirect, render
from .models import *
from .forms import ProfileModelForm
from django.views.generic import ListView
from django.contrib.auth.models import  User

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
    senders= list(map(lambda x:x.sender, invites))
    is_empty= False
    if len(senders) ==0:
        is_empty=True

    context={
        'senders':senders,
        'is_empty':is_empty,
    }

    return render(request, 'profile/invites.html', context)

def accept_invites(request):
    if request.method =='POST':
        pk= request.POST.get('sender_pk')
        sender =Profiles.objects.get(pk=pk)
        receiver = Profiles.objects.get(user=request.user)
        friendship = get_object_or_404(Friendship, sender=sender, receiver=receiver)
        if friendship.friendship_status =='send':
            friendship.friendship_status='accepted'
            friendship.save()
    return redirect('profile:invites')


def reject_invite(request):
    if request.method =='POST':
        pk= request.POST.get('sender_pk')
        sender =Profiles.objects.get(pk=pk)
        receiver = Profiles.objects.get(user=request.user)
        friendship = get_object_or_404(Friendship, sender=sender, receiver=receiver)
        friendship.delete()
    return redirect('profile:invites')

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

    def get_queryset(self):
        profiles=Profiles.objects.get_profiles(user=self.request.user)
        return profiles

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user=User.objects.get(username__iexact=str(self.request.user))
        profile=Profiles.objects.get(user=user)
        friendships=Friendship.objects.all()
        friendship_we_sender=Friendship.objects.filter(sender=profile)
        friendship_we_receiver=Friendship.objects.filter(receiver=profile)
        sent_request_list=[]
        received_request_list=[]

        for friendship in friendship_we_sender:
            sent_request_list.append(friendship.receiver.user)
        for friendship in friendship_we_receiver:
            received_request_list.append(friendship.sender.user)

        context['sent_request_list']=sent_request_list
        context['received_request_list']=received_request_list
        context['is_empty'] = False
        if len(self.get_queryset())==0:
            context['is_empty'] = True
        
        print("sent request list ")
        print(sent_request_list)
        print("@@@@@@@@@@@@")
        print("recieved request list")
        print(received_request_list)
        print("@@@@@@@@@@@@")
        print("friendships")
        print(friendships)
        print("###################")
        print("frienship we sender")
        print(friendship_we_sender)
        print("###################")
        print("frienship we receiver")
        print(friendship_we_receiver)

        return context
    


def profiles_available_for_invites(request):
    sender=request.user
    profiles=Profiles.objects.get_profiles_available_for_invite(sender=sender)
    user=request.user
    profile=Profiles.objects.get(user=user)
    friendship_we_sender=Friendship.objects.filter(sender=profile)
    friendship_we_receiver=Friendship.objects.filter(receiver=profile)
    sent_request_list=[]
    received_request_list=[]

    for friendship in friendship_we_sender:
        sent_request_list.append(friendship.receiver.user)
    for friendship in friendship_we_receiver:
        received_request_list.append(friendship.sender.user)

    context ={
        'profiles':profiles,
        'sent_request_list':sent_request_list,
        'received_request_list':received_request_list
    }
    return render(request, 'profile/availables.html', context)

def  send_friend_request(request):
    if request.method == 'POST':
        pk= request.POST.get('profile_pk')
        user=request.user
        sender=Profiles.objects.get(user=user)
        receiver=Profiles.objects.get(pk=pk)

        friendship=Friendship.objects.create(sender=sender, receiver=receiver, friendship_status='send')
        return redirect(request.META.get('HTTP_REFERER'))
    return redirect('profile:profile_view')

def remove_from_friends(request):
    if request.method == 'POST':
        pk = request.POST.get('profile_pk')
        user=request.user
        sender=Profiles.objects.get(user=user)
        receiver=Profiles.objects.get(pk=pk)

        friendship=Friendship.objects.get(
            (Q(sender=sender) & Q(receiver=receiver) | Q(sender=receiver) & Q(receiver=sender))
        )
        friendship.delete()
        return redirect(request.META.get('HTTP_REFERER'))
    return redirect('profile:profile_view')