from django.urls import path
from .views import *

app_name = 'ichoose'
urlpatterns = [
    path('', index, name='ichoose_home'),
    path('shop/', product_grid, name='ichoose_product_grid'),
    path('product/<int:id>/', single_product, name='ichoose_product'),
    path('wishlist/<int:id>/', wishlist, name='wishlist'),
    path('add_to_cart/<int:id>/', add_to_cart, name='add_to_cart'),
    path('show_wishlist/', show_wishlist, name='show_wishlist'),
    path('cart/', mycart, name='mycart'),
    path('remove/<int:id>/', remove, name='remove'),
    path('search/', search, name='search'),
    path('add_comments/<int:id>/', add_comment, name='add_comment'),
    path('shipping_details/', HomePageView.as_view(), name='shipping_details'),
    path('remove_wish/<int:id>/', remove_wish, name='remove_wish'),

    path('paayment/', charge, name='charge'),
    path('seller_api/', SellerVerifyAPI.as_view(), name='seller_verify'),
    path('verify_api/', SellVerifyAPI.as_view(), name='sell_verify'),
    path('flutter/', flutter_verify, name='flutter'),
    path('profile/', profile, name='profile'),

    path('customization_requests_buyer/', customization_requests_buyer, name='customization_requests_buyer')

]