from abc import abstractproperty
from django.urls import path
from .views import  *

app_name='profile'

urlpatterns = [
   path('', profile_view, name='profile_view'),
   path("invites/", requests_view, name="invites" ),
   path('profiles/', ProfilesListView.as_view(), name='profiles'),
   path('availables/', profiles_available_for_invites, name='availables'),
   path('send-request/', send_friend_request, name='send-request'),
   path('delete-friend/', remove_from_friends, name='remove-friend' ),
   path('invites/accept/', accept_invites, name='accept-invites'),
   path('invites/reject/', reject_invite, name='reject-invites'),
] 