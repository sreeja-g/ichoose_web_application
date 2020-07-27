from djongo import models
from django import forms
from registration.models import User

class lenders(models.Model):
    lender = models.OneToOneField(User, on_delete=models.CASCADE, related_name='lender_user_id')


class lenders_form(forms.ModelForm):
    class Meta:
        model = lenders
        fields = (
            'lender',
        )


class offlinewallet(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_id_offlinewallet')

    price = models.IntegerField()
    # remain_priceforloans=models.IntegerField(default=0)


class lcards(models.Model):
    lender = models.OneToOneField(lenders, on_delete=models.CASCADE, related_name='lender_user_id_lcards')
    no_of_cards = models.ListField(default=[])
    money = models.ListField(default=[])
    
class lender_details(models.Model):
    lender = models.IntegerField(default=0)
    loan_amount=models.IntegerField(default=0)
    loan_on_order_id=models.IntegerField(default=0)
    