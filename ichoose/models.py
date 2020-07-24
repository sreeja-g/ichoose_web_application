from djongo import models
from registration.models import User
from django import forms
from ichoose.list_field import CustomListField

#_______________________________________________abstract_models_____________________________________________



class order_details_abs(models.Model):

    product_title = models.TextField()
    category_1 = models.TextField()
    category_2 = models.TextField()
    product_description = models.TextField()

    product_name = models.TextField()
    product_detail = models.TextField()
    product_color = models.TextField()
    product_size = models.TextField()
    product_price = models.FloatField()
    product_discount = models.FloatField()
    product_final_price = models.FloatField()

    product_remaining_details = CustomListField(default=[])
    images = CustomListField(default=[])

    class Meta:
        abstract = True


class order_details_abs_form(forms.ModelForm):
    class Meta:
        model = order_details_abs

        fields = (
            'product_title',
            'category_1','category_2','product_description','images','product_remaining_details','product_name','product_detail','product_color',
            'product_size','product_price','product_discount','product_final_price',
        )


class order_abs(models.Model):

    order_id=models.IntegerField()
    buyer_id = models.IntegerField()
    product_id = models.IntegerField()

    date_of_order = models.DateTimeField()
    told_date_of_order = models.DateTimeField()
    date_of_delivery = models.DateTimeField()

    order_details = models.EmbeddedField(model_container=order_details_abs,model_form_class=order_details_abs_form)

    quantity = models.IntegerField(null=False)
    total_price = models.TextField()

    payment_status = models.BooleanField(default=False)
    delivery_status = models.BooleanField(default=False)

    loan_status = models.BooleanField(default=False)
    loan_amount = models.IntegerField(default=None)

    cancel_status = models.BooleanField(default=False)
    cancel_date = models.DateTimeField()
    class Meta:
        abstract = True

class order_abs_form(forms.ModelForm):
    class Meta:
        model = order_abs

        fields = ('order_id','buyer_id', 'product_id', 'date_of_order',
                  'told_date_of_order', 'date_of_delivery', 'order_details', 'quantity', 'total_price',
                  'payment_status',
                  'delivery_status', 'loan_status', 'loan_amount','cancel_status','cancel_date'
                  )



class ratings_comments_abs(models.Model):
    ratings_comments_id=models.IntegerField()
    buyer_id = models.IntegerField()
    product_id=models.IntegerField()
    user_name = models.CharField()
    date_time = models.DateTimeField()

    verified_user=models.BooleanField(default=False)

    like= models.BooleanField(default=False)
    comment=models.TextField()
    rating=models.IntegerField()

    reply=models.TextField()
    reply_timestamp=models.DateTimeField()

    class Meta:
        abstract = True

class ratings_comments_abs_form(forms.ModelForm):
    class Meta:
        model = ratings_comments_abs

        fields = ('ratings_comments_id','buyer_id', 'product_id','date_time', 'verified_user',
                  'like', 'comment', 'rating','reply','reply_timestamp'
                  )


class loan_abs(models.Model):
    loan_id=models.IntegerField()
    order_id = models.IntegerField()
    seller_id=models.IntegerField()


    loan_applied_date = models.DateTimeField()
    loan_status = models.BooleanField(default=False)
    loan_amount = models.IntegerField(default=None)
    loan_intrest = models.IntegerField()

    loan_returned_status = models.BooleanField(default=False)
    loan_returned_date = models.DateTimeField()

    class Meta:
        abstract = True

class loan_abs_form(forms.ModelForm):
    class Meta:
        model = loan_abs

        fields = ('loan_id','order_id','seller_id','loan_applied_date', 'loan_status', 'loan_amount','loan_intrest','loan_returned_status','loan_returned_date'
                  )


class customization_abs(models.Model):
    customization_id= models.IntegerField()
    buyer_id=models.IntegerField()
    product_id = models.IntegerField()

    date_time = models.DateTimeField()

    customization_details = CustomListField(default=[])
    request_status = models.BooleanField(default=False)

    accepted_details=CustomListField(default=[])
    accept_status=models.BooleanField(default=False)
    reject_status=models.BooleanField(default=False)

    order_id = models.IntegerField(default=None)

    class Meta:
        abstract = True

class customization_abs_form(forms.ModelForm):
    class Meta:
        model = customization_abs

        fields = ('customization_id','buyer_id','product_id','date_time', 'customization_details', 'request_status','accepted_details','accept_status','reject_status','order_id'
                  )


class product_abs(models.Model):

    product_id=models.IntegerField()
    seller_id=models.IntegerField()

    date_of_post = models.DateTimeField()

    product_title = models.TextField()
    category_1 = models.TextField()
    category_2 = models.TextField()
    product_description = models.TextField()

    product_name = models.TextField()
    product_detail = models.TextField()
    product_color = CustomListField(default=[])
    product_size = models.TextField()
    product_price = models.FloatField()
    product_discount = models.FloatField()
    product_final_price = models.FloatField()

    product_remaining_details = CustomListField(default=[])
    additional_information=models.TextField()

    images = CustomListField(default=[])

    product_customisation_available= CustomListField(default=[])
    additional_customization_information=models.TextField()

    order_list=models.ArrayField(model_container=order_abs,model_form_class=order_abs_form,default=[])
    ratings_comments=models.ArrayField(model_container=ratings_comments_abs,model_form_class=ratings_comments_abs_form,default=[])
    customization_requests_list=models.ArrayField(model_container=customization_abs,model_form_class=customization_abs_form,default=[])

    class Meta:
        abstract = True

class product_abs_form(forms.ModelForm):
    class Meta:
        model = product_abs

        fields = (
            'product_id','seller_id', 'date_of_post', 'product_title',
            'category_1','category_2','product_description','images','product_remaining_details','product_name','product_detail','product_color',
            'product_size','product_price','product_discount','product_final_price',
            'additional_information','product_customisation_available','additional_customization_information',
            'order_list','ratings_comments','customization_requests_list'
        )
#___________________________________________________________________________________________________________




class buyers(models.Model):

    buyer=models.OneToOneField(User, on_delete=models.CASCADE,related_name='buyer_user_id')

    #shipping_details

    order_list=models.ArrayField(model_container=order_abs,model_form_class=order_abs_form,default=[])
    ratings_comments=models.ArrayField(model_container=ratings_comments_abs,model_form_class=ratings_comments_abs_form,default=[])
    customization_requests_list=models.ArrayField(model_container=customization_abs,model_form_class=customization_abs_form,default=[])

    objects = models.DjongoManager()

class buyers_form(forms.ModelForm):
    class Meta:
        model = buyers
        fields = (
            'buyer',
        )



class seller_verification_process(models.Model):

    seller=models.OneToOneField(User, on_delete=models.CASCADE,related_name='seller_id_verification_process')

    name= models.CharField(max_length=100)
    phone_number=models.CharField(max_length=50)

    address_line_1 = models.CharField(max_length=100)
    address_line_2 = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pincode = models.CharField(max_length=50)

    purpose = models.TextField()

    images = models.ListField(default=[])
    files = models.ListField(default=[])

    Verification_step_1 = models.BooleanField(default=False)
    Verification_step_2 = models.BooleanField(default=False)
    Verification_step_3 = models.BooleanField(default=False)



class sellers(models.Model):

    seller=models.OneToOneField(User, on_delete=models.CASCADE,related_name='seller_user_id')

    product_list=models.ArrayField(model_container=product_abs,model_form_class=product_abs_form,default=[])
    order_list=models.ArrayField(model_container=order_abs,model_form_class=order_abs_form,default=[])
    loan_list=models.ArrayField(model_container=loan_abs,model_form_class=loan_abs_form,default=[])
    customization_requests_list=models.ArrayField(model_container=customization_abs,model_form_class=customization_abs_form,default=[])

    objects = models.DjongoManager()

class sellers_form(forms.ModelForm):
    class Meta:
        model = sellers
        fields = (
            'seller','product_list','order_list','loan_list','customization_requests_list'
        )



class product(models.Model):

    seller = models.ForeignKey(sellers, on_delete=models.CASCADE, related_name='seller_id_product')

    date_of_post = models.DateTimeField()

    product_title = models.TextField()
    category_1 = models.TextField()
    category_2 = models.TextField()
    product_description = models.TextField()
    product_name=models.TextField()
    product_detail=models.TextField()
    product_color=CustomListField(default=[])
    product_size=models.TextField()
    product_price=models.FloatField()
    product_discount=models.FloatField()
    product_final_price=models.FloatField()

    product_remaining_details= CustomListField(default=[])
    additional_information=models.TextField()

    images = CustomListField(default=[])

    product_customisation_available= CustomListField(default=[])
    additional_customization_information=models.TextField()

    order_list=models.ArrayField(model_container=order_abs,model_form_class=order_abs_form,default=[])
    ratings_comments=models.ArrayField(model_container=ratings_comments_abs,model_form_class=ratings_comments_abs_form,default=[])
    customization_requests_list=models.ArrayField(model_container=customization_abs,model_form_class=customization_abs_form,default=[])

    objects = models.DjongoManager()

class product_form(forms.ModelForm):
    class Meta:
        model = product
        fields = (
            'seller', 'date_of_post', 'product_title',
            'category_1','category_2','product_description','images','product_remaining_details','product_name','product_detail','product_color',
            'product_size','product_price','product_discount','product_final_price','additional_information','product_customisation_available','additional_customization_information',
        )


class ratings_comments(models.Model):
    buyer = models.ForeignKey(buyers, on_delete=models.CASCADE, related_name='buyer_id_ratings_comments')
    product = models.ForeignKey(product, on_delete=models.CASCADE, related_name='product_id_ratings_comments')
    user_name = models.CharField(max_length = 255)
    date_time=models.DateTimeField()

    verified_user = models.BooleanField(default=False)

    like = models.BooleanField(default=False)
    comment = models.TextField()
    rating = models.IntegerField()

    reply = models.TextField()
    reply_timestamp = models.DateTimeField()




class ratings_comments_form(forms.ModelForm):
    class Meta:
        model = ratings_comments

        fields = ('buyer', 'product','date_time', 'verified_user',
                  'like', 'comment', 'rating', 'reply','reply_timestamp'
                  )


class customization(models.Model):

    buyer = models.ForeignKey(buyers, on_delete=models.CASCADE, related_name='buyer_id_customization')
    product = models.ForeignKey(product, on_delete=models.CASCADE, related_name='product_id_customization')

    date_time = models.DateTimeField()

    customization_details = CustomListField(default=[])
    request_status = models.BooleanField(default=False)

    accepted_details = CustomListField(default=[])
    accept_status = models.BooleanField(default=False)
    reject_status = models.BooleanField(default=False)

    order_id = models.IntegerField(default=None)



class customization_form(forms.ModelForm):
    class Meta:
        model = customization

        fields = ('buyer','product','date_time', 'customization_details', 'request_status','accepted_details','accept_status','reject_status','order_id'
                  )

class order(models.Model):

    buyer = models.ForeignKey(buyers, on_delete=models.CASCADE, related_name='buyer_id_order')
    product = models.ForeignKey(product, on_delete=models.SET_NULL, null=True, related_name='product_id_order')

    date_of_order = models.DateTimeField()
    told_date_of_order = models.DateTimeField()
    date_of_delivery = models.DateTimeField()

    order_details = models.EmbeddedField(model_container=order_details_abs,model_form_class=order_details_abs_form)

    quantity = models.IntegerField(null=False)
    total_price=models.TextField()

    payment_status = models.BooleanField(default=False)
    delivery_status = models.BooleanField(default=False)

    loan_status = models.BooleanField(default=False)
    loan_amount = models.IntegerField(default=None)

    cancel_status = models.BooleanField(default=False)
    cancel_date = models.DateTimeField()

    objects = models.DjongoManager()

class order_form(forms.ModelForm):
    class Meta:
        model = order
        fields = ('buyer','product', 'date_of_order',
            'told_date_of_order','date_of_delivery','order_details','quantity','total_price','payment_status',
            'delivery_status','loan_status','loan_amount'
        )


class loan(models.Model):
    order = models.OneToOneField(order, on_delete=models.CASCADE, related_name='order_id_loan')
    seller = models.ForeignKey(sellers, on_delete=models.CASCADE, related_name='seller_id_loan')

    loan_applied_date = models.DateTimeField()
    loan_status = models.BooleanField(default=False)
    loan_amount = models.IntegerField(default=None)
    loan_intrest = models.IntegerField()

    loan_returned_status=models.BooleanField(default=False)
    loan_returned_date=models.DateTimeField()

class loan_form(forms.ModelForm):
    class Meta:
        model = loan

        fields = ('order', 'seller','loan_applied_date', 'loan_status', 'loan_amount','loan_intrest','loan_returned_status','loan_returned_date'
                  )



from django.dispatch import receiver
from django.db.models.signals import post_save,pre_delete

@receiver(post_save, sender=order)
def create_or_update_order(sender, instance, created, **kwargs):
    if created:

        new = order_abs(order_id=instance.id)
        new.buyer_id=instance.buyer.id
        new.product_id = instance.product.id

        new.date_of_order = instance.date_of_order
        new.told_date_of_order = instance.told_date_of_order

        new.order_details = instance.order_details

        new.quantity = instance.quantity
        new.total_price = instance.total_price

        seller_order=instance.product.seller
        seller_order.order_list.append(new)
        seller_order.save()

        product_order=instance.product
        product_order.order_list.append(new)
        product_order.save()

        buyer_order=instance.buyer
        buyer_order.order_list.append(new)
        buyer_order.save()
    else:

        seller_order = instance.product.seller
        seller_order_list=seller_order.order_list

        for i in range(len(seller_order_list)):
            if seller_order_list[i].order_id==instance.id:

                new = order_abs(order_id=instance.id)
                new.buyer_id = instance.buyer.id
                new.product_id = instance.product.id

                new.date_of_order = instance.date_of_order
                new.told_date_of_order = instance.told_date_of_order
                new.date_of_delivery = instance.date_of_delivery

                new.order_details = instance.order_details

                new.quantity = instance.quantity
                new.total_price = instance.total_price

                new.payment_status = instance.payment_status
                new.delivery_status = instance.delivery_status
                new.loan_status = instance.loan_status
                new.loan_amount = instance.loan_amount

                new.cancel_status = instance.cancel_status
                new.cancel_date = instance.cancel_date

                seller_order_list[i]=new
                break
        seller_order.save()

        product_order = instance.product
        product_order_list = product_order.order_list

        for i in range(len(product_order_list)):
            if product_order_list[i].order_id == instance.id:
                new = order_abs(order_id=instance.id)
                new.buyer_id = instance.buyer.id
                new.product_id = instance.product.id

                new.date_of_order = instance.date_of_order
                new.told_date_of_order = instance.told_date_of_order
                new.date_of_delivery = instance.date_of_delivery

                new.order_details = instance.order_details

                new.quantity = instance.quantity
                new.total_price = instance.total_price

                new.payment_status = instance.payment_status
                new.delivery_status = instance.delivery_status
                new.loan_status = instance.loan_status
                new.loan_amount = instance.loan_amount

                new.cancel_status = instance.cancel_status
                new.cancel_date = instance.cancel_date

                product_order_list[i] = new
                break
        product_order.save()

        buyer_order = instance.buyer
        buyer_order_list = buyer_order.order_list

        for i in range(len(buyer_order_list)):
            if buyer_order_list[i].order_id == instance.id:
                new = order_abs(order_id=instance.id)
                new.buyer_id = instance.buyer.id
                new.product_id = instance.product.id

                new.date_of_order = instance.date_of_order
                new.told_date_of_order = instance.told_date_of_order
                new.date_of_delivery = instance.date_of_delivery

                new.order_details = instance.order_details
                new.quantity = instance.quantity
                new.total_price = instance.total_price

                new.payment_status = instance.payment_status
                new.delivery_status = instance.delivery_status
                new.loan_status = instance.loan_status
                new.loan_amount = instance.loan_amount

                new.cancel_status = instance.cancel_status
                new.cancel_date = instance.cancel_date

                buyer_order_list[i] = new
                break
        buyer_order.save()


# @receiver(pre_delete, sender=order)
# def delete_order(sender, instance,  **kwargs):
#     seller_order = instance.product.seller
#     seller_order_list = seller_order.order_list
#
#     for i in range(len(seller_order_list)):
#         if seller_order_list[i].order_id == instance.id:
#
#             del(seller_order_list[i])
#
#             break
#     seller_order.save()
#
#     product_order = instance.product
#     product_order_list = product_order.order_list
#
#     for i in range(len(product_order_list)):
#         if product_order_list[i].order_id == instance.id:
#
#             del(product_order_list[i])
#
#             break
#     product_order.save()
#
#     buyer_order = instance.buyer
#     buyer_order_list = buyer_order.order_list
#
#     for i in range(len(buyer_order_list)):
#         if buyer_order_list[i].order_id == instance.id:
#
#             del (buyer_order_list[i])
#
#             break
#     buyer_order.save()


@receiver(post_save, sender=ratings_comments)
def create_or_update_ratings_and_comments(sender, instance, created, **kwargs):
    if created:

        new_ratings_comments = ratings_comments_abs()
        new_ratings_comments.ratings_comments_id=instance.id
        new_ratings_comments.buyer_id = instance.buyer.id
        new_ratings_comments.product_id = instance.product.id
        new_ratings_comments.user_name = instance.user_name
        new_ratings_comments.date_time=instance.date_time

        new_ratings_comments.verified_user = instance.verified_user  # if buyer bought that product
        new_ratings_comments.like = instance.like
        new_ratings_comments.comment = instance.comment
        new_ratings_comments.rating = instance.rating

        product_ratings_comments = instance.product
        product_ratings_comments.ratings_comments.append(new_ratings_comments)
        product_ratings_comments.save()

        buyer_ratings_comments = instance.buyer
        buyer_ratings_comments.ratings_comments.append(new_ratings_comments)
        buyer_ratings_comments.save()

    else:

        product_ratings_comments = instance.product
        product_ratings_comments_list = product_ratings_comments.ratings_comments

        for i in range(len(product_ratings_comments_list)):
            if product_ratings_comments_list[i].ratings_comments_id == instance.id:
                new_ratings_comments = ratings_comments_abs()
                new_ratings_comments.ratings_comments_id = instance.id
                new_ratings_comments.buyer_id = instance.buyer.id
                new_ratings_comments.product_id = instance.product.id

                new_ratings_comments.date_time = instance.date_time

                new_ratings_comments.verified_user = instance.verified_user  # if buyer bought that product
                new_ratings_comments.like = instance.like
                new_ratings_comments.comment = instance.comment
                new_ratings_comments.rating = instance.rating

                new_ratings_comments.reply = instance.reply
                new_ratings_comments.reply_timestamp = instance.reply_timestamp

                product_ratings_comments_list[i]=new_ratings_comments
                break
        product_ratings_comments.save()

        buyer_ratings_comments = instance.buyer
        buyer_ratings_comments_list = buyer_ratings_comments.ratings_comments

        for i in range(len(buyer_ratings_comments_list)):
            if buyer_ratings_comments_list[i].ratings_comments_id == instance.id:
                new_ratings_comments = ratings_comments_abs()
                new_ratings_comments.ratings_comments_id = instance.id
                new_ratings_comments.buyer_id = instance.buyer.id
                new_ratings_comments.product_id = instance.product.id

                new_ratings_comments.date_time = instance.date_time

                new_ratings_comments.verified_user = instance.verified_user  # if buyer bought that product
                new_ratings_comments.like = instance.like
                new_ratings_comments.comment = instance.comment
                new_ratings_comments.rating = instance.rating

                new_ratings_comments.reply = instance.reply
                new_ratings_comments.reply_timestamp = instance.reply_timestamp

                buyer_ratings_comments_list[i]=new_ratings_comments
                break
        buyer_ratings_comments.save()


@receiver(pre_delete, sender=ratings_comments)
def delete_ratings_comments(sender, instance,  **kwargs):

    product_ratings_comments = instance.product
    product_ratings_comments_list = product_ratings_comments.ratings_comments

    for i in range(len(product_ratings_comments_list)):
        if product_ratings_comments_list[i].ratings_comments_id == instance.id:

            del(product_ratings_comments_list[i])

            break
    product_ratings_comments.save()

    buyer_ratings_comments = instance.buyer
    buyer_ratings_comments_list = buyer_ratings_comments.ratings_comments

    for i in range(len(buyer_ratings_comments_list)):
        if buyer_ratings_comments_list[i].ratings_comments_id == instance.id:

            del (buyer_ratings_comments_list[i])

            break
    buyer_ratings_comments.save()


@receiver(post_save, sender=customization)
def create_or_update_customization(sender, instance, created, **kwargs):
    if created:

        new_customization = customization_abs()
        new_customization.customization_id=instance.id
        new_customization.buyer_id=instance.buyer.id
        new_customization.product_id = instance.product.id
        new_customization.date_time = instance.date_time
        new_customization.customization_details = instance.customization_details

        seller_customization = instance.product.seller
        seller_customization.customization_requests_list.append(new_customization)
        seller_customization.save()

        product_customization = instance.product
        product_customization.customization_requests_list.append(new_customization)
        product_customization.save()

        buyer_customization = instance.buyer
        buyer_customization.customization_requests_list.append(new_customization)
        buyer_customization.save()

    else:

        seller_customization = instance.product.seller
        seller_customization_list = seller_customization.customization_requests_list

        for i in range(len(seller_customization_list)):
            if seller_customization_list[i].customization_id == instance.id:
                new_customization = customization_abs()
                new_customization.customization_id = instance.id
                new_customization.buyer_id = instance.buyer.id
                new_customization.product_id = instance.product.id
                new_customization.date_time = instance.date_time
                new_customization.customization_details = instance.customization_details

                new_customization.request_status = instance.request_status
                new_customization.accepted_details = instance.accepted_details
                new_customization.accept_status = instance.accept_status
                new_customization.reject_status = instance.reject_status
                new_customization.order_id = instance.order_id

                seller_customization_list[i]=new_customization
                break
        seller_customization.save()

        buyer_customization = instance.buyer
        buyer_customization_list = buyer_customization.customization_requests_list

        for i in range(len(buyer_customization_list)):
            if buyer_customization_list[i].customization_id == instance.id:
                new_customization = customization_abs()
                new_customization.customization_id = instance.id
                new_customization.buyer_id = instance.buyer.id
                new_customization.product_id = instance.product.id
                new_customization.date_time = instance.date_time
                new_customization.customization_details = instance.customization_details

                new_customization.request_status = instance.request_status
                new_customization.accepted_details = instance.accepted_details
                new_customization.accept_status = instance.accept_status
                new_customization.reject_status = instance.reject_status
                new_customization.order_id = instance.order_id

                buyer_customization_list[i] = new_customization
                break
        buyer_customization.save()

        product_customization = instance.product
        product_customization_list = product_customization.customization_requests_list

        for i in range(len(product_customization_list)):
            if product_customization_list[i].customization_id == instance.id:
                new_customization = customization_abs()
                new_customization.customization_id = instance.id
                new_customization.buyer_id = instance.buyer.id
                new_customization.product_id = instance.product.id
                new_customization.date_time = instance.date_time
                new_customization.customization_details = instance.customization_details

                new_customization.request_status = instance.request_status
                new_customization.accepted_details = instance.accepted_details
                new_customization.accept_status = instance.accept_status
                new_customization.reject_status = instance.reject_status
                new_customization.order_id = instance.order_id

                product_customization_list[i] = new_customization
                break
        product_customization.save()


@receiver(post_save, sender=loan)
def create_or_update_loan(sender, instance, created, **kwargs):
    if created:

        new_loan = loan_abs()
        new_loan.loan_id = instance.id
        new_loan.order_id=instance.order.id
        new_loan.seller_id = instance.seller.id

        new_loan.loan_applied_date=instance.loan_applied_date
        new_loan.loan_status=instance.loan_status
        new_loan.loan_amount = instance.loan_amount

        seller_loan = instance.seller
        seller_loan.loan_list.append(new_loan)
        seller_loan.save()

    else:

        seller_loan = instance.seller
        seller_loan_list = seller_loan.loan_list

        for i in range(len(seller_loan_list)):
            if seller_loan_list[i].loan_id == instance.id:

                new_loan = loan_abs()
                new_loan.loan_id = instance.id
                new_loan.order_id = instance.order.id
                new_loan.seller_id = instance.seller.id

                new_loan.loan_applied_date = instance.loan_applied_date
                new_loan.loan_status = instance.loan_status
                new_loan.loan_amount = instance.loan_amount

                new_loan.loan_returned_status = instance.loan_returned_status
                new_loan.loan_returned_date = instance.loan_returned_date

                seller_loan_list[i]=new_loan
                break
        seller_loan.save()
