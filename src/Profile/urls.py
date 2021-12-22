from abc import abstractproperty
from django.urls import path
from .views import  *

app_name='profile'

urlpatterns = [
   path('', profile_view, name='profile_view'),
   path("invites/", requests_view, name="invites" ),
   path('profiles/', profile_list_view, name='profiles'),
   path('availables/', profiles_available_for_invites, name='availables')
] 