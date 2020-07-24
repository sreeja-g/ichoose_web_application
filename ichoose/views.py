from django.contrib.auth.decorators import login_required
from django.shortcuts import HttpResponse, get_object_or_404, redirect, render
from .models import *
from isell.models import *
from ilend.models import *
from datetime import datetime
from django.contrib import messages
from django.urls import reverse
from django.http import HttpResponseRedirect
import stripe
from django.conf import settings
from django.views.generic.base import TemplateView
from django.db.models import Q
from .category_types import categories
from rest_framework import generics,filters
from ichoose.serializers import SellerVerify,SellUserVerify
from ichoose.models import seller_verification_process
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
stripe.api_key ='sk_test_51H85ctJGt48B5LYp9cViFLQ9g8LtffZM4oAKsbu6ImxJ68NMZpkzuOq8sj2VbL7HBB0dHvBmthZG6RQkspKnUE7R00Uv7mugNb'
#home page



class SellerVerifyAPI(generics.ListCreateAPIView):
    filter_backends = (filters.SearchFilter,)
    queryset = seller_verification_process.objects.all()
    serializer_class = SellerVerify


class  SellVerifyAPI(generics.ListCreateAPIView):
    filter_backends = (filters.SearchFilter,)
    queryset = seller_verification_process.objects.all()
    serializer_class = SellUserVerify

@csrf_exempt
def flutter_verify(request):
    body_unicode = request.body.decode('utf-8')
    final_dictionary = eval(body_unicode)
    p=seller_verification_process.objects.filter(name=final_dictionary['name'])[0]
    p.Verification_step_1 = final_dictionary['Verification_step_1']
    p.Verification_step_2 = final_dictionary['Verification_step_2']
    p.Verification_step_3 = final_dictionary['Verification_step_3']
    if p.Verification_step_1 == p.Verification_step_2 == p.Verification_step_3 == 'True':
        User.verification_status = 'True'
    else:
        User.verification_status = 'False'
    p.save()
    return None

@login_required(login_url='/login/')
def profile(request):
    buyer_profile = buyers.objects.all()
    context = {
        'buyer_profile': buyer_profile
    }
    return render(request, 'profile.html',context)




def index(request):
    inital = {"items":[],"price":0.0,"count":0}
    session = request.session.get("data", inital)
    product_wish = product.objects.filter(id__in=session["items"])
    count_cart= session["count"]
    cart_price = session["price"]
    context ={
        'product_wish':product_wish,'count_cart':count_cart,'categories' : categories,
    }
    return render(request, 'index-v2.html',context)


#shop
def product_grid(request):
    products = None
    inital = {"items":[],"price":0.0,"count":0}
    session = request.session.get("data", inital)
    product_wish = product.objects.filter(id__in=session["items"])
    count_cart= session["count"]
    cart_price = session["price"]
    cate = request.GET.get('category_1')
    cate_2 = request.GET.get('category_2')
    if cate:
        products = product.objects.filter(Q(category_1__exact=cate) | Q(category_2__exact=cate_2))
    else:
        products = product.objects.all()
    context={
        'product': products,
        'product_wish':product_wish,'count_cart':count_cart,
        'cart_price':cart_price,
        'categories' : categories,
        "title": cate 
    } 
    return render(request, 'shop.html',context)

# deatil view
def single_product(request, id=None):
    # instance = product.objects.get(id=1)
    instance = get_object_or_404(product,id=id)

    
    buyer_usernames=[]
    for each in instance.ratings_comments:
        buyer_usernames.append(buyers.objects.get(pk=each.buyer_id).buyer.username)
    data = zip(instance.ratings_comments,buyer_usernames)

    inital = {"items":[],"price":0.0,"count":0}
    session = request.session.get("data", inital)
    product_wish = product.objects.filter(id__in=session["items"])
    count_cart= session["count"]
    cart_price = session["price"] 
    context={
        'product':instance,
        'data':data,
        'product_wish':product_wish,'count_cart':count_cart,
    }
    return render(request,'single-product.html',context)

#search

def search(request):
    q = request.GET["search"]
    products = product.objects.filter(Q(product_title__icontains=q) | Q(product_name__icontains=q))
    inital = {"items":[],"price":0.0,"count":0}
    session = request.session.get("data", inital)
    product_wish = product.objects.filter(id__in=session["items"])
    count_cart= session["count"]
    cart_price = session["price"] 
    context = {"product": products,
            'product_wish':product_wish,'count_cart':count_cart,
        'cart_price':cart_price,
        "title": q + " - search",
        'categories' : categories,}  #for title of web page

    return render(request, "shop.html", context)
#wishlist
def wishlist(request,id=None):
    
    inital = {"items":[],"price":0.0,"count":0}
    session1 = request.session.get("data", inital)
    session2 = request.session.get("mywishlist",inital)
    cart_count = seaaion1["count"]
    product_ = product.objects.get(id=id)
    if id in session1["items"]:
        messages.error(request, "Already in cart")
    else:
        session2["items"].append(id)
        request.session["mywishlist"] = session2
    products = product.objects.filter(id__in=session2["items"])

    context = {
        'product':products,
        'count_cart':cart_count,
    }
    return redirect('ichoose:ichoose_product_grid')

def show_wishlist(request):
    inital = {"items":[],"price":0.0,"count":0}
    sess = request.session.get("mywishlist", inital)
    session = request.session.get("data", inital)
    products = product.objects.filter(id__in=sess["items"])
    count_cart= session["count"]

    context = {"products": products,
                'count_cart': count_cart,
            }
    return render(request, "wishlist.html", context)

def add_to_cart(request, id=None):
    """
        data = {"items" : ["slug1", "slug2"],
                "price" : 12342,
                "count" : 5
                }
        request.session["data"] = data
    """
        
    
    inital = {"items":[],"price":0.0,"count":0}
    session = request.session.get("data", inital)
    # session["price"] = 0.0
    # session["count"] = 0
    session2 = request.session.get("mywishlist", inital)
    product_ = product.objects.get(id=id)
    if id in session["items"]:
        messages.error(request, "Already added to cart")
    elif id in session2["items"]:
        session2["items"].remove(id)
        session["items"].append(id)
        session["price"] += float(product_.product_final_price)
        session["count"] += 1
        request.session["data"] = session
    else:
        session["items"].append(id)
        session["price"] += float(product_.product_final_price)
        session["count"] += 1
        request.session["data"] = session
        
    products = product.objects.filter(id__in=session["items"])
    count_cart= session["count"]
    
    # return HttpResponseRedirect(reverse('ichoose:ichoose_product_grid',kwargs={'product_wish':products,'count_cart':count_cart,}))
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def mycart(request):
    inital = {"items":[],"price":0.0,"count":0}
    sess = request.session.get("data", inital)
    products = product.objects.filter(id__in=sess["items"])
    count_cart= sess["count"]
    context = {"products": products,
                "count_cart":count_cart,
            }
    return render(request, "shop-cart.html", context)

def remove_wish(request,id):
    inital = {"items":[],"price":0.0,"count":0}

    session = request.session.get("mywishlist", inital)
    product_ = product.objects.get(id=id)
    if id in session["items"]:
        session["items"].remove(id)
        session["price"] -= float(product_.product_final_price)
        session["count"] -= 1
        request.session["mywishlist"] = session
    
    products = product.objects.filter(id__in=session["items"])
    
    context = {"products": products,
            }
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def remove(request,id):
    inital = {"items":[],"price":0.0,"count":0}

    session = request.session.get("data", inital)
    product_ = product.objects.get(id=id)
    if id in session["items"]:
        session["items"].remove(id)
        session["price"] -= float(product_.product_final_price)
        session["count"] -= 1
        request.session["data"] = session
    
    products = product.objects.filter(id__in=session["items"])
    
    context = {"products": products,
            }
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def add_comment(request,id):
    
    if request.method == 'POST':
        user = request.user
        name_user = user.username
        comment_reviews = ratings_comments()
        
        if user is None:
            messages.error(request, "login to comment")
        else:
            
            comment_reviews.buyer_id = user.pk
            comment_reviews.product_id = id
            comment_reviews.user_name = name_user
            comment_reviews.date_time = datetime.now()
            comment_user = request.POST.get('review-text')
            
            comment_reviews.comment = comment_user
            rating_user = request.POST.get('star-box')
            comment_reviews.rating = rating_user
            reply = "-"
            comment_reviews.reply = reply
            comment_reviews.reply_timestamp = datetime.now()
            comment_reviews.save()
            

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def shipping_details(request):
    inital = {"items":[],"price":0.0,"count":0}
    sess = request.session.get("data", inital)
    products = product.objects.filter(id__in=sess["items"])
    count_cart= sess["count"]
    context = {"products": products,
    "count_cart":count_cart,'categories' : categories,
        }
    return render(request,'shop-checkout.html',context)
class HomePageView(TemplateView):
    template_name = 'shop-checkout.html'

    def get_context_data(self, **kwargs): # new
        context = super().get_context_data(**kwargs)
        context['key'] ='pk_test_51H85ctJGt48B5LYpJLPUNMnBk8F9AQdGn4Jt2MBhIA2G104PM6ke8DmL7ghTYmMyUbJK6YBYhecT029wgk4ikcZe00zFOfCNl6'
       
        return context

def charge(request): # new
    print('923888888888888888888888888888888')
    print(request.POST['stripeToken'])
    inital = {"items":[],"price":0.0,"count":0}
    session = request.session.get("data", inital)
    price_ = int(session["price"])
    print(price_)
    if request.method == 'POST':
        
        charge = stripe.Charge.create(
            amount= price_ ,
            currency='inr',
            description='A Django charge',
            source=request.POST['stripeToken']
            
        )
        
        products = product.objects.filter(id__in=session["items"])
        for p in products:
            order_create = order()
            buyer_ = buyers.objects.get(buyer=request.user)
            order_create.buyer = buyer_
            order_create.product = p
            order_create.date_of_order = datetime.now()
            
            order_create.quantity = 1
            order_create.total_price = p.product_final_price * order_create.quantity
            order_create.payment_status = True
            x = order_details_abs(product_title=p.product_title,category_1= p.category_1,category_2=p.category_2,product_description=p.product_description,product_name=p.product_name,product_color=p.product_color,product_detail=p.product_detail,product_size=p.product_size,product_price=p.product_price,product_discount=p.product_discount,product_final_price=p.product_final_price,product_remaining_details=p.product_remaining_details,images=p.images)
            order_create.order_details = x
            order_create.save()
            id_ = p.pk
            if id_ in session["items"]:
                session["items"].remove(id_)
                session["price"] -= float(p.product_final_price)
                session["count"] -= 1
                request.session["data"] = session
        count_cart = session["count"]
        a=offlinewallet.objects.get(user=User.objects.filter(is_superuser=True)[0])
        a.price=a.price+int(session["price"])
        a.save(update_fields=int(session['price']))
        context={'price':session["price"],"count_cart":count_cart,'categories' : categories,}
        
        return render(request, 'order-tracking.html',context=context)
    print('---------------')
    print(settings.STRIPE_PUBLISHABLE_KEY)