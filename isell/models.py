from djongo import models
from registration.models import User
from django import forms
from ichoose.list_field import CustomListField
from ichoose.models import seller_verification_process, sellers, sellers_form, product, product_form, ratings_comments, ratings_comments_form, customization, customization_form, order, order_form, loan, loan_form
from django.dispatch import receiver
from django.db.models.signals import post_save,pre_delete
from ilend.models import lenders,offlinewallet
from ichoose.models import product_abs, buyers

@receiver(post_save, sender=User)
def create_or_update_user(sender, instance, created, **kwargs):
    if created:
        new_buyer=buyers(buyer=instance)
        new_buyer.save()
        new_lender = lenders(lender=instance)
        new_lender.save()
        new_wallet = offlinewallet(user=instance, price=0)
        new_wallet.save()


@receiver(post_save, sender=product)
def create_or_update_product(sender, instance, created, **kwargs):
    if created:
        new_product_abs=product_abs(product_id=instance.id)
        new_product_abs.seller_id=instance.seller.id

        new_product_abs.date_of_post = instance.date_of_post

        new_product_abs.product_title = instance.product_title
        new_product_abs.category_1 = instance.category_1
        new_product_abs.category_2 = instance.category_2
        new_product_abs.product_description = instance.product_description

        new_product_abs.images = instance.images

        new_product_abs.product_name = instance.product_name
        new_product_abs.product_detail = instance.product_detail
        new_product_abs.product_color = instance.product_color
        new_product_abs.product_size = instance.product_size
        new_product_abs.product_price = instance.product_price
        new_product_abs.product_discount = instance.product_discount
        new_product_abs.product_final_price = instance.product_final_price

        new_product_abs.product_remaining_details = instance.product_remaining_details

        new_product_abs.additional_information = instance.additional_information
        new_product_abs.product_customisation_available = instance.product_customisation_available
        new_product_abs.additional_customization_information = instance.additional_customization_information

        new_product_abs.order_list = instance.order_list
        new_product_abs.ratings_comments = instance.ratings_comments
        new_product_abs.customization_requests_list = instance.customization_requests_list

        instance.seller.product_list.append(new_product_abs)
        instance.seller.save()

    else:

        products_seller = instance.seller
        products_seller_list=products_seller.product_list

        for i in range(len(products_seller_list)):
            if products_seller_list[i].product_id==instance.id:

                new_product_abs = product_abs(product_id=instance.id)
                new_product_abs.seller_id = instance.seller.id

                new_product_abs.date_of_post = instance.date_of_post

                new_product_abs.product_title = instance.product_title
                new_product_abs.category_1 = instance.category_1
                new_product_abs.category_2 = instance.category_2
                new_product_abs.product_description = instance.product_description

                new_product_abs.images = instance.images

                new_product_abs.product_name = instance.product_name
                new_product_abs.product_detail = instance.product_detail
                new_product_abs.product_color = instance.product_color
                new_product_abs.product_size = instance.product_size
                new_product_abs.product_price = instance.product_price
                new_product_abs.product_discount = instance.product_discount
                new_product_abs.product_final_price = instance.product_final_price

                new_product_abs.product_remaining_details = instance.product_remaining_details

                new_product_abs.additional_information = instance.additional_information
                new_product_abs.product_customisation_available = instance.product_customisation_available
                new_product_abs.additional_customization_information = instance.additional_customization_information

                new_product_abs.order_list = instance.order_list
                new_product_abs.ratings_comments = instance.ratings_comments
                new_product_abs.customization_requests_list = instance.customization_requests_list

                products_seller_list[i]=new_product_abs
                break
        products_seller.save()

@receiver(pre_delete, sender=product)
def delete_product(sender, instance,  **kwargs):

    products_seller = instance.seller
    products_seller_list=products_seller.product_list

    for i in range(len(products_seller_list)):
        if products_seller_list[i].product_id==instance.id:

            del(products_seller_list[i])

            break
    products_seller.save()


