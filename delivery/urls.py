from django.contrib.auth import views
from django.urls import path
from .views import *


urlpatterns = [
    path('order/', OrderAPIView.as_view(), name="order"),
    path('deliver/', deliver_verify,name ="deliver"),
]