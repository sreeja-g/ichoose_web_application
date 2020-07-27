from rest_framework import serializers

from ichoose.models import seller_verification_process


class SellerVerify(serializers.ModelSerializer):
    class Meta:
        model = seller_verification_process
        fields = ('city','name','address_line_1','address_line_2','seller')


class SellUserVerify(serializers.ModelSerializer):
    class Meta:
        model = seller_verification_process
        fields = ('Verification_step_1','Verification_step_2','Verification_step_3','name')

    def get_request(self):
        print(self.context)