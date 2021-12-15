from abc import abstractproperty
from django.urls import path
from .views import  *

app_name='profile'

urlpatterns = [
   path('', profile_view, name='profile_view')
] 