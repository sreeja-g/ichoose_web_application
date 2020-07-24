from django.shortcuts import render
from django.conf import settings 
from .models import *
from ichoose.models import sellers
from django.views.generic.base import TemplateView

import stripe
# Create your views here.
# stripe.api_key = settings.STRIPE_SECRET_KEY
stripe.api_key ='sk_test_51H85ctJGt48B5LYp9cViFLQ9g8LtffZM4oAKsbu6ImxJ68NMZpkzuOq8sj2VbL7HBB0dHvBmthZG6RQkspKnUE7R00Uv7mugNb'


def display_home(request):
    loan_money=0
    money=0
    k=offlinewallet.objects.all()
    if len(k)>0:
      print(lenders.objects.get(lender=request.user).lender)
      p=offlinewallet.objects.filter(user=lenders.objects.get(lender=request.user).lender)
      if len(p)>0:
        m1=lcards.objects.filter(lender=lenders.objects.get(lender=request.user))
        if(len(m1)>0):
                for i in range(len(m1[0].money)):
                    loan_money+=m1[0].money[i]*m1[0].no_of_cards[i]
                
            
                
                context={'price':int(p[0].price)-loan_money,'user':lenders.objects.get(lender=request.user).lender}

        else:
            context={'price':int(p[0].price),'user':lenders.objects.get(lender=request.user).lender}
      else:
            context={'price':0,'user':lenders.objects.get(lender=request.user).lender}
        
      return render(request,'loan_interface/loan_home.html',context=context)
    else:
        context={'price':0,'user':lenders.objects.get(lender=request.user).lender}
        
        
        return render(request,'loan_interface/loan_home.html',context=context)
#to show left over money
def displaycard(request):
    loan_money=0
    g=offlinewallet.objects.all()
    if(len(g)>0):
        p=offlinewallet.objects.get(user=lenders.objects.get(lender=request.user).lender)
        m=lcards.objects.filter(lender=lenders.objects.get(lender=request.user))
        if(len(m)>0):
                for i in range(len(m[0].money)):
                    loan_money+=m[0].money[i]*m[0].no_of_cards[i]
                if(int(p.price)-loan_money==0):
                    context={'price':int(p.price)-loan_money,'value':0,'user':lenders.objects.get(lender=request.user).lender}
                
                else:
                    context={'price':int(p.price)-loan_money,'user':lenders.objects.get(lender=request.user).lender}

        else:
            context={'price':int(p.price), 'user':lenders.objects.get(lender=request.user).lender}
        
        return render(request,'loan_interface/add_cards.html',context=context)
    else:
         context={'price':0,'value':0,'user':lenders.objects.get(lender=request.user).lender}
        
         return render(request,'loan_interface/add_cards.html',context=context)
# to show card
def viewcard(request):
    loan_money=0
    a=offlinewallet.objects.all()
    if len(a)>0:
        p=offlinewallet.objects.get(user=lenders.objects.get(lender=request.user).lender)
        m=lcards.objects.filter(lender=lenders.objects.get(lender=request.user))
        dict1={25:0,50:0,75:0,100:0,125:0,150:0,175:0,200:0}
        money_list=[]
        cards_list=[]
        if(len(m)>0):
                for i in range(len(m[0].money)):
                    money_list.append(int(m[0].money[i]))
                    cards_list.append(int(m[0].no_of_cards[i]))
                for  j in dict1.keys():
                 for i in range(len(money_list)):
                    if(j==money_list[i]):
                        dict1[j]+=cards_list[i]
                print(dict1)
                
                
                context={"context":dict1,'user':lenders.objects.get(lender=request.user).lender}

        else:
            context={"context":dict1,'user':lenders.objects.get(lender=request.user).lender}
        return render(request,'loan_interface/view_cards.html',context=context)
    else:
        dict1={25:0,50:0,75:0,100:0,125:0,150:0,175:0,200:0}
        context={"context":dict1,'user':lenders.objects.get(lender=request.user).lender}
        return render(request,'loan_interface/view_cards.html',context=context)

# to add card in database

def addcard(request):
   loan_money=0
   
   if request.method == 'POST': 

        cards = request.POST.get('cards')
        money=request.POST.get('money') 
        g=offlinewallet.objects.all()
        
        print(lcards.objects.all())
        if len(g)>0:
            p=offlinewallet.objects.get(user=lenders.objects.get(lender=request.user).lender)
            print(p.price)
            y=lcards.objects.filter(lender=lenders.objects.get(lender=request.user))
            if len(y)>0:
                for i in range(len(y[0].money)):
                    loan_money+=y[0].money[i]*y[0].no_of_cards[i]
                
                if(int(p.price)-(int(loan_money)+(int(cards)*int(money)))<0):
                   return render(request,'loan_interface/add_cards.html')
                else:
                 print("a")
                 print(money in y[0].money)
                 if money in y[0].money :
                    print("a")
                    print(y[0].money)
                    y[0].no_of_cards[y[0].money.index(money)]+=int(cards)
                    
                    a=offlinewallet.objects.get(user=User.objects.filter(is_superuser=True)[0])
                    print(a)
                    a.price+=(int(cards)*int(money))
                    a.save(update_fields=['price'])
                    p.remain_priceforloans=(p.remain_priceforloans-(int(cards)*int(money)))
                    p.save()
                   
                    y[0].save(update_fields=['no_of_cards'])
                 else:
                    print("b")
                    y[0].money.append(int(money))
                    y[0].no_of_cards.append(int(cards))
                    
                    a=offlinewallet.objects.get(user=User.objects.filter(is_superuser=True)[0])
                    a.price+=(int(cards)*int(money))
                    a.save(update_fields=['price'])
                    p.remain_priceforloans=(p.remain_priceforloans-(int(cards)*int(money)))
                    p.save()
                    y[0].save()
                          

            else:
                
                print(int(p.price)-(int(cards)*int(money)))
                if(int(p.price)-(int(cards)*int(money))<0):
                   print(int(p.price)-(int(money)))
                   return render(request,'loan_interface/add_cards.html')
                else:
                    
                    a=offlinewallet.objects.get(user=User.objects.filter(is_superuser=True)[0])
                    
                    a.price+=(int(cards)*int(money))
                    a.save(update_fields=['price'])
                    p.remain_priceforloans=(p.remain_priceforloans-(int(cards)*int(money)))
                    p.save()

                    lcards.objects.create(lender=lenders.objects.get(lender=request.user),money=[int(money)],no_of_cards=[int(cards)])

                    
        
            return render(request,'loan_interface/loan_home.html')
        
       
        
            
       
        
   
   
#stripe charges editing over
class HomePageView(TemplateView):
    template_name = 'loan_interface/add_money.html'

    def get_context_data(self, **kwargs): # new
        context = super().get_context_data(**kwargs)
        context['key'] = 'pk_test_51H85ctJGt48B5LYpJLPUNMnBk8F9AQdGn4Jt2MBhIA2G104PM6ke8DmL7ghTYmMyUbJK6YBYhecT029wgk4ikcZe00zFOfCNl6'#settings.STRIPE_PUBLISHABLE_KEY
        
        
        return context
def charge(request): # new
       if request.method == 'POST':
        charge = stripe.Charge.create(
            amount=int(request.POST.get('price'))*100,
            currency='inr',
            description='A Django charge',
            source=request.POST['stripeToken']
        ),
        username = lenders.objects.get(lender=request.user).lender
        price=request.POST.get('price')
        p=offlinewallet.objects.filter(user=lenders.objects.get(lender=request.user).lender)
       
        if len(p)>0:
            p1=offlinewallet.objects.get(user=lenders.objects.get(lender=request.user).lender) 
            p1.price = p1.price+int(price)
            p1.remain_priceforloans=p1.price
            p1.save()
        else:
            p=offlinewallet(username=username,price=price,remain_priceforloans=price)
            p.save()
      
        context={'price':request.POST.get('price')}
        return render(request, 'loan_interface/charge.html',context=context)

        

def sub_lists(list1): 
  
    # store all the sublists  
    sublist = [[]] 
      
    # first loop  
    for i in range(len(list1) + 1): 
          
        # second loop  
        for j in range(i + 1, len(list1) + 1): 
              
            # slice the subarray  
            sub = list1[i:j] 
            sublist.append(sub)
              
      
    return sublist 
b=lcards.objects.all()
possible_money=[]
for i in range(len(b)):
        print(b[i].no_of_cards,b[i].money)
        for j in range(len(b[i].no_of_cards)):
            for k in range((b[i].no_of_cards[j])):
              possible_money.append(str(b[i].money[j]))
possible_money2=[]
for i in possible_money:
    possible_money2.append(int(i))
subsets=sub_lists(possible_money2)
sum_subsets=[]
for i in subsets:
    sum_subsets.append(sum(i))
# print(sum_subsets)
mylist = list(dict.fromkeys(sum_subsets))
print(mylist)

# def money_loan(mon,lost_cards,p):
#     print(p,sum(lost_cards))
#     if(p==sum(lost_cards)):
#         a1=offlinewallet.objects.get(username="admin")
#         a1.price=a1.price-sum(lost_cards)
#         a1.save(update_fields=['price'])
#         return -1
#     else:
#             m1=lcards.objects.all()
        
#             for i in range(len(m1)):
                   
#                 if mon in m1[i].money and m1[i].no_of_cards[m1[i].money.index(mon)]>0:
#                     m1[i].no_of_cards[m1[i].money.index(mon)]-=1
#                     m1[i].save(update_fields=['no_of_cards'])
#                     lost_cards.append(mon)
#                     print(m1[i].name)
#                     print("----------")
#                     print(lost_cards)
#             if(mon==0):
#                 mon=200
            
#             if (p-sum(lost_cards)) in possible_money2:
#               return money_loan(mon-25,lost_cards,p)
#             else:
#                 max=100
#                 k=0
#                 result=[i for i in possible_money2 if not i in lost_cards or lost_cards.remove(i)]
#                 print("result",result)
#                 for i in result:

#                     if((p-sum(lost_cards)-i<max)):
#                         max=(p-sum(lost_cards))-i
#                         k=i
#                         print("k",k)
#                 return money_loan(mon-25,lost_cards,p)
def  money_loan(p):
    print(p)              
    subsets=sub_lists(possible_money2)
    sum_subsets=[]
    possible_cards=[]
    max=0
    actual_card=[]
    for i in subsets:
        if(sum(i)==p):
            possible_cards.append(i)
    for i in possible_cards:
        if(len(i)>max):
            max=len(i)
            actual_card=i
    print("actualcard",actual_card)
    m1=lcards.objects.all()
    nested_cards=[]
    for i in range(len(m1)):
        nested_cards.append([])
        for j in range(len(m1[i].no_of_cards)):
            for k in range((m1[i].no_of_cards[j])):

                nested_cards[i].append(m1[i].money[j])
    print(nested_cards)
    count=0
    for i in sorted(actual_card):
        print(i)
        if(count==len(nested_cards)):
            print("if")
            count=0
            nested_cards[count].remove(i)
            count=count+1
        else:
             print("else")
             if i in nested_cards[count]:
                nested_cards[count].remove(i)
                count=count+1
             else:
                if(count<len(nested_cards)-1):
                 count=count+1
                 nested_cards[count].remove(i)
                else:
                    count=0
                    nested_cards[count].remove(i)

                 
        print(nested_cards)
        for i in range(len(m1)):
            for j in m1[i].money:
                 m1[i].no_of_cards[m1[i].money.index(j)]=nested_cards[i].count(j)
                 m1[i].save(update_fields=['no_of_cards'])

   
    a1=offlinewallet.objects.get(user=User.objects.filter(is_superuser=True)[0])
    a1.price=a1.price-p
    a1.save(update_fields=['price'])
    k=offlinewallet.objects.get(user=sellers.objects.get(seller=order_.product).seller) 
    print(k.price)
    k.price=k.price+p
    k.save()        

from ichoose.models import order,loan
import datetime

def loan_taken(order_id,amount,accept):

    order_=order.objects.get(pk=order_id)
    print(order_id,amount,accept)

    if accept==False:
        p=float(order_.total_price)/2
    else:
        p=amount



    a=offlinewallet.objects.get(user=User.objects.filter(is_superuser=True)[0])

    if accept==False:

        if (a.price > p):
        
           
            # print(p in mylist)
            flag = 0
            for i in mylist:
            
                if (p == i):
                    print("money is detecting")
                    flag = 1
                    money_loan(p)

                    break
            if (flag == 0):
                for i in mylist:
                    if p < i:
                    
                        print("money has to add")
                        return (False, i)
                    if(i==mylist[-1] and p>i):
                        return(False,i)

            else:
                
                return (False, p)



        else:

            return (False, a.price)

    else:
        

        if (a.price > p):
            
            flag = 0
            for i in mylist:
                if (p == i):
                    print("money is detecting")
                    flag = 1
                    money_loan(p)

                    break
            if (flag == 0):
                for i in mylist:
                    if p < i:
                        print("money has to add")

                        new_loan = loan()
                        new_loan.order = order_
                        new_loan.seller = order_.product.seller
                        new_loan.loan_intrest=5
                        new_loan.loan_applied_date = datetime.datetime.now()
                        new_loan.loan_status = True
                        new_loan.loan_amount = i

                        new_loan.save()

                        order_.loan_status = True
                        order_.loan_amount = i
                        order_.save()

                        return (True, i)


            else:

                new_loan = loan()
                new_loan.order = order_
                new_loan.seller = order_.product.seller
                new_loan.loan_intrest=5
                new_loan.loan_applied_date = datetime.datetime.now()
                new_loan.loan_status = True
                new_loan.loan_amount = p

                new_loan.save()

                order_.loan_status = True
                order_.loan_amount = p
                order_.save()
                return (True, p)



        else:

            new_loan = loan()
            new_loan.order = order_
            new_loan.seller = order_.product.seller
            new_loan.loan_intrest=5
            new_loan.loan_applied_date = datetime.datetime.now()
            new_loan.loan_status = True
            new_loan.loan_amount = a.price

            new_loan.save()

            order_.loan_status = True
            order_.loan_amount = a.price
            order_.save()
            return (True, a.price)



    

   
