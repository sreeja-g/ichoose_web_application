from django.urls import path
from .views import *
urlpatterns = [
    path('isell/home/', isell_home, name='isell_home'),
    path('isell/verification_request/', verification_request, name='verification_request'),
    path('isell/add_products/', add_products, name='add_products'),
    path('isell/add_new_product/', add_new_product, name='add_new_product'),
    path('isell/edit_product/', edit_product, name='edit_product'),
    path('isell/remove_product/', remove_product, name='remove_product'),


    path('isell/loan_details/', loan_details, name='loan_details'),
    path('isell/write_reply/', write_reply, name='write_reply'),
    path('isell/reply_customization_requests/', reply_customization_requests,
         name='reply_customization_requests'),
    path('isell/accept_reject_customization_requests/', accept_reject_customization_requests, name='accept_reject_customization_requests'),
    path('isell/customization_requests/', customization_requests, name='customization_requests'),
    path('isell/show_product/', show_product, name='show_product'),
    path('isell/delivered_products/', delivered_products, name='delivered_products'),
    path('isell/applied_loans/', applied_loans, name='applied_loans'),
    path('isell/show_order/', show_order, name='show_order'),
    path('isell/apply_loan/', apply_loan, name='apply_loan'),

    path('isell/export_data/', export_data, name='export_data'),
    path('isell/statistics/', statistics, name='statistics'),
]