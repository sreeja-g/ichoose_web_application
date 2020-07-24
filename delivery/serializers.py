from rest_framework import serializers
from delivery.models import order_Search


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = order_Search
        fields = '__all__'