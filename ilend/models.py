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


class lcards(models.Model):
    lender = models.OneToOneField(lenders, on_delete=models.CASCADE, related_name='lender_user_id_lcards')
    no_of_cards = models.ListField(default=[])
    money = models.ListField(default=[])


