from djongo import models
from registration.models import User


class order_Search(models.Model):
    order_id=models.IntegerField()
    product_id = models.IntegerField()
    is_packed = models.BooleanField(default= False)
    is_dispatched = models.BooleanField(default= False)
    is_shipped= models.BooleanField(default= False)
    is_delivered = models.BooleanField(default= False)