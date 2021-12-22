from abc import abstractproperty
from django.urls import path
from .views import  *

app_name='post'

urlpatterns = [
    path('', post_comment_list_view, name='post_view'),
    path('like/', like_unlike_post, name='like_view'),
    path('<pk>/delete/', PostDeleteView.as_view(), name="delete")
] 