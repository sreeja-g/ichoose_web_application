from django.shortcuts import HttpResponse, get_object_or_404, redirect, render
from .models import *
from isell.models import *
from datetime import datetime
from django.contrib import messages
from django.urls import reverse
from django.http import HttpResponseRedirect

def index(request):
    inital = {"items":[],"price":0.0,"count":0}
    session = request.session.get("data", inital)
    product_wish = product.objects.filter(id__in=session["items"])
    count_cart= session["count"]
    cart_price = session["price"]
    context ={
        'product_wish':product_wish,'count_cart':count_cart,
    }
    return render(request, 'index-v2.html',context)



def product_grid(request):
    products = product.objects.all()
    inital = {"items":[],"price":0.0,"count":0}
    session = request.session.get("data", inital)
    product_wish = product.objects.filter(id__in=session["items"])
    count_cart= session["count"]
    cart_price = session["price"] 
    context={
        'product': products,
        'product_wish':product_wish,'count_cart':count_cart,
        'cart_price':cart_price,
    }
    return render(request, 'shop.html',context)


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


def search(request):
    q = request.GET["search"]
    products = product.objects.filter(product_title__icontains=q)
    inital = {"items":[],"price":0.0,"count":0}
    session = request.session.get("data", inital)
    product_wish = product.objects.filter(id__in=session["items"])
    count_cart= session["count"]
    cart_price = session["price"] 
    context = {"product": products,
            'product_wish':product_wish,'count_cart':count_cart,
        'cart_price':cart_price,
        "title": q + " - search"}  #for title of web page
    return render(request, "shop.html", context)

def wishlist(request,id=None):
    
    inital = {"items":[],"price":0.0,"count":0}
    session1 = request.session.get("data", inital)
    session2 = request.session.get("mywishlist",inital)
    product_ = product.objects.get(id=id)
    if id in session1["items"]:
        messages.error(request, "Already in cart")
    else:
        session2["items"].append(id)
        request.session["mywishlist"] = session2
    products = product.objects.filter(id__in=session2["items"])
    context = {
        'product':products,
        
    }
    return redirect('ichoose:ichoose_product_grid')

def show_wishlist(request):
    inital = {"items":[],"price":0.0,"count":0}
    sess = request.session.get("mywishlist", inital)
    products = product.objects.filter(id__in=sess["items"])
    
    context = {"products": products,
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
    
    context = {"products": products,
            }
    return render(request, "shop-cart.html", context)

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
    if request.method == 'POST':
        shipping = buyers()
        ship = shipping.shipping_details()
        ship.first_name = request.POST.get('first-name-2')

        

    return render(request,'shop-checkout.html')
