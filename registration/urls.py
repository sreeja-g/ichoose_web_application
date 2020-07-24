from .views import *
from django.urls import path

urlpatterns = [
    path('', index, name='index'),
    path('home/', home, name='home'),
    path('login/', user_login, name='login'),
    path('signup/', signup, name='signup'),
    path('logout/', user_logout, name='logout'),
    path(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
         activate, name='activate'),
    path('forgot_password/', forgot_password, name='forgot_password'),
    path(r'^reset_password_url_verification/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
         reset_password_url_verification, name='reset_password_url_verification'),
    path('reset_password/', reset_password, name='reset_password'),
    path('api/', OrderAPIView.as_view(), name='user_api'),

]