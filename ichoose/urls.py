from django.urls import path
from .views import *
urlpatterns = [
    path('', index , name='ichoose_home'),
    path('shop/' ,product_grid ,name='ichoose_product_grid' ),
    path('product/<int:id>/' ,single_product ,name='ichoose_product' ),
    path('wishlist/<int:id>/',wishlist,name='wishlist'),
    path('add_to_cart/<int:id>/',add_to_cart ,name='add_to_cart'),
    path('show_wishlist/',show_wishlist,name='show_wishlist'),
    path('cart/',mycart,name='mycart'),
    path('remove/<int:id>/',remove ,name='remove'),
    path('search/',search, name='search'),
    path('add_comments/<int:id>/',add_comment ,name='add_comment'),


]