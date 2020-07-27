from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics,filters
from delivery.models import order_Search
from delivery.serializers import OrderSerializer
from ichoose.models import order
from ilend.views import money_return

class OrderAPIView(generics.ListCreateAPIView):
    filter_backends = (filters.SearchFilter, )
    queryset = order_Search.objects.all()
    serializer_class = OrderSerializer


@csrf_exempt
def deliver_verify(request):
    print(request.body)
    body_unicode = request.body.decode('utf-8')
    print(type(body_unicode))
    final_dictionary = eval(body_unicode)
    print(final_dictionary)
    p=order_Search.objects.filter(order_id=final_dictionary['order_id'])
    for i in range(len(p)):
     if(p[i].product_id==final_dictionary['product_id']):
        p[i].is_packed= final_dictionary['is_packed']
        p[i].is_dispatched = final_dictionary['is_dispatched']
        p[i].is_shipped= final_dictionary['is_shipped']
        p[i].is_delivered= final_dictionary['is_delivered']
        p[i].save()
        if p[i].is_delivered == 'True':
            money_return(final_dictionary['order_id'])
            k = order.objects.get(pk = final_dictionary['order_id'])
            k.order.deliver_status = 'True'
            k.save()
        else:
            order.deliver_status = 'False'
        p[i].save()
    return redirect(reverse('isell:isell_home'))
