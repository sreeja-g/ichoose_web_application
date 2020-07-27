from rest_framework import serializers
from registration.models import User
from ichoose.models import seller_verification_process

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email','password','address','id')

