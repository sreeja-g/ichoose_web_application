from django.shortcuts import render
from rest_framework import generics,filters
from delivery.models import order_Search
from delivery.serializers import OrderSerializer

class OrderAPIView(generics.ListCreateAPIView):
    filter_backends = (filters.SearchFilter, )
    queryset = order_Search.objects.all()
    serializer_class = OrderSerializer