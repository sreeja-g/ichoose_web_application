from django.urls import path

from . import views
app_name='loan_interface'


urlpatterns = [
    path('ilend/home/',views.display_home,name='home'),
    path('ilend/', views.HomePageView.as_view(), name='wallet'),
    path('ilend/charge/', views.charge, name='charge'),
    path('ilend/card/', views.addcard, name='card'),
    path('ilend/display_card/', views.displaycard, name='displaycard'),
    path('ilend/view_card/', views.viewcard, name='viewcard'),

]