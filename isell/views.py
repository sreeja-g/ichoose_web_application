from django.shortcuts import render,redirect, HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required,user_passes_test
from isell.models import seller_verification_process,sellers,product
from ichoose.models import buyers,customization,order,ratings_comments,loan
from django.core.files.storage import FileSystemStorage
from django.urls import reverse
import datetime,json
from django.contrib import messages
import csv
from .graphs import get_chart
from django.db.models import Count
from ichoose.category_types import categories

from ilend.models import offlinewallet, lenders


def test_verification(user):
    if user.verification_status==True:
        return True
    else:
        return False

def test_verification_application(user):
    if user.verification_applied==False:
        return True
    else:
        return False


@login_required(login_url='/login/')
def export_data(request):

    if request.method == "POST":
        user = request.user
        
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="ichoose_data.csv"'

        writer = csv.writer(response, delimiter=',')

        if request.POST.get('export_data_type') == "add_products":

            if request.POST.get('export_data_time_selected') and request.POST.get('export_data_time_selected')!="" and request.POST.get('export_data_time_selected')!="100":
                items = product.objects.filter(seller=sellers.objects.get(seller=user), date_of_post__gte=datetime.datetime.now()-datetime.timedelta(days=int(request.POST.get('export_data_time_selected')))).order_by('-date_of_post') if len(product.objects.filter(seller=sellers.objects.get(seller=user), date_of_post__gte=datetime.datetime.now()-datetime.timedelta(days=int(request.POST.get('export_data_time_selected'))))) > 0 else []
            else:
                items = product.objects.filter(seller=sellers.objects.get(seller=user)).order_by('-date_of_post') if len(product.objects.filter(seller=sellers.objects.get(seller=user))) > 0 else []


            writer.writerow(['Product_title', 'Product_category_1', 'Product_category_2', 'Product_final_price', 'Product_date_of_post', 'Product_number_of_orders'])

            for obj in items:
                writer.writerow([obj.product_title, obj.category_1, obj.category_2, obj.product_final_price, obj.date_of_post, len(obj.order_list) ])

        if request.POST.get('export_data_type') == "delivered_products":

            days_selected_time_filter =  request.POST.get('export_data_time_selected') 

            seller = sellers.objects.get(seller=request.user)
            items = []

            for each in seller.order_list:
                if each.delivery_status == True:
                    if days_selected_time_filter != "" and days_selected_time_filter != "100":
                        if (datetime.datetime.now() - each.date_of_order).days < int(days_selected_time_filter):
                            items.append(each)
                    else:     
                        items.append(each)

            writer.writerow(['Product_title', 'Product_category_1', 'Product_category_2', 'Product_final_price', 'Product_date_of_post', 'Product_number_of_orders'])

            for obj in items:
                writer.writerow([obj.product_title, obj.category_1, obj.category_2, obj.product_final_price, obj.date_of_post, len(obj.order_list) ])

        if request.POST.get('export_data_type') == "applied_loans":

            days_selected_time_filter =  request.POST.get('export_data_time_selected') 

            seller = sellers.objects.get(seller=request.user)
            items = []
            print("********************************************************")
            print(seller)
            for each in seller.loan_list:
                if days_selected_time_filter != "" and days_selected_time_filter != "100":
                    if (datetime.datetime.now() - each.loan_applied_date).days < int(days_selected_time_filter):
                        items.append(each)
                else:     
                    items.append(each)


            writer.writerow(['Order_id', 'loan amount', 'interest', 'loan status', 'loan applied date time', 'loan returned status', 'loan returned date time'])

            for obj in items:
                writer.writerow([obj.order_id, obj.loan_amount, obj.loan_intrest, obj.loan_status, obj.loan_applied_date, obj.loan_returned_status, obj.loan_returned_date ])

        if request.POST.get('export_data_type') == "pending_orders":

            days_selected_time_filter =  request.POST.get('export_data_time_selected') 

            seller=sellers.objects.filter(seller=request.user)
            items=[]
            try:
                for each in seller[0].order_list:
                    if each.delivery_status==False:
                        if days_selected_time_filter != "" and days_selected_time_filter != "100":
                            if (datetime.datetime.now() - each.date_of_order).days < int(days_selected_time_filter):
                                items.append(each)
                        else:     
                            items.append(each)
            except:
                pass


            writer.writerow(['Order product title', 'Order product name', 'price', 'quantity', 'total', 'order time', 'delivery deadline'])

            for obj in items:
                writer.writerow([obj.order_details.product_title, obj.order_details.product_name, obj.order_details.product_final_price, obj.quantity, obj.total_price, obj.date_of_order, obj.told_date_of_order ])


        return response

    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

@login_required(login_url='/login/')
def isell_home(request):

    days_selected_time_filter = ""
    time_filter_dict = {'1':0, '3':1,'7':2,'30':3,'100':4}
    time_filter_list=["","","","","selected"]

    if request.method == 'POST':
        if request.POST.get('time') and (request.POST.get('time') in time_filter_dict.keys()):
            days_selected_time_filter = request.POST.get('time')
            time_filter_list=["","","","",""]   
            time_filter_list[time_filter_dict[request.POST.get('time')]] = "selected"

    seller=sellers.objects.filter(seller=request.user)
    pending_orders=[]
    try:
        for each in seller[0].order_list:
            if each.delivery_status==False:
                if days_selected_time_filter != "" and days_selected_time_filter != "100":
                    if (datetime.datetime.now() - each.date_of_order).days < int(days_selected_time_filter):
                        pending_orders.append(each)
                else:     
                    pending_orders.append(each)
    except:
        pass
    count = 0
    try:
        for each in seller[0].customization_requests_list:
            if each.accept_status == False and each.reject_status == False:
                count += 1
    except:
        pass

    walet_value = offlinewallet.objects.filter(user=lenders.objects.get(lender=request.user).lender)[0].price if offlinewallet.objects.filter(user=lenders.objects.get(lender=request.user).lender)[0].price else 0

    return render(request, 'index3.html',{'pending_orders':pending_orders,'count':count,'date':datetime.datetime.now(),'time_filter_list':time_filter_list, 'days_selected_time_filter':days_selected_time_filter, 'walet_value' : walet_value})

@login_required(login_url='/login/')
def statistics(request):
    
    product_chart_data = product.objects.filter(seller=sellers.objects.get(seller=request.user)).values('date_of_post').annotate(Count('id')).order_by('date_of_post')
    # print(product_chart_data[0])
    product_chart_data = product_chart_data[:100] if len(product_chart_data) > 100 else product_chart_data
    product_chart_data_month_year_filtered = {}
    for each in product_chart_data:
        if str(each['date_of_post'].day)+'_'+str(each['date_of_post'].month)+'_'+str(each['date_of_post'].year) in product_chart_data_month_year_filtered.keys():
            product_chart_data_month_year_filtered[str(each['date_of_post'].day)+'_'+str(each['date_of_post'].month)+'_'+str(each['date_of_post'].year)] += each['id__count']
        else:
            product_chart_data_month_year_filtered[str(each['date_of_post'].day)+'_'+str(each['date_of_post'].month)+'_'+str(each['date_of_post'].year)] = each['id__count']

    products_chart = get_chart(product_chart_data_month_year_filtered,'your_products')

    # print(products_chart.as_html())

    orders_chart_data=[]
    for each in sellers.objects.get(seller=request.user).product_list:
        orders_chart_data.extend(order.objects.filter(product=each.product_id).values('date_of_order').annotate(Count('id')).order_by('date_of_order'))

    print(orders_chart_data)
    orders_chart_data_month_year_filtered = {}
    for each in orders_chart_data : 
        if str(each['date_of_order'].day)+'_'+str(each['date_of_order'].month)+'_'+str(each['date_of_order'].year) in orders_chart_data_month_year_filtered.keys():
            orders_chart_data_month_year_filtered[str(each['date_of_order'].day)+'_'+str(each['date_of_order'].month)+'_'+str(each['date_of_order'].year)] += each['id__count']
        else:
            orders_chart_data_month_year_filtered[str(each['date_of_order'].day)+'_'+str(each['date_of_order'].month)+'_'+str(each['date_of_order'].year)] = each['id__count']

    orders_chart = get_chart(orders_chart_data_month_year_filtered,'your_orders')

    # print(orders_chart.as_html())

    orders_delivered_chart_data=[]
    for each in sellers.objects.get(seller=request.user).product_list:
        orders_delivered_chart_data.extend(order.objects.filter(product=each.product_id, delivery_status=True).values('date_of_order').annotate(Count('id')).order_by('date_of_order'))

    print(orders_delivered_chart_data)
    orders_delivered_chart_data_month_year_filtered = {}
    for each in orders_delivered_chart_data : 
        if str(each['date_of_order'].day)+'_'+str(each['date_of_order'].month)+'_'+str(each['date_of_order'].year) in orders_chart_data_month_year_filtered.keys():
            orders_delivered_chart_data_month_year_filtered[str(each['date_of_order'].day)+'_'+str(each['date_of_order'].month)+'_'+str(each['date_of_order'].year)] += each['id__count']
        else:
            orders_delivered_chart_data_month_year_filtered[str(each['date_of_order'].day)+'_'+str(each['date_of_order'].month)+'_'+str(each['date_of_order'].year)] = each['id__count']

    orders_delivered_chart = get_chart(orders_delivered_chart_data_month_year_filtered,'your_delivered_orders')

    print(orders_delivered_chart.as_html())

    walet_value = offlinewallet.objects.filter(user=lenders.objects.get(lender=request.user).lender)[0].price if offlinewallet.objects.filter(user=lenders.objects.get(lender=request.user).lender)[0].price else 0
    
    return render(request, 'statistics.html',{'products_chart':products_chart,'orders_chart':orders_chart, 'orders_delivered_chart':orders_delivered_chart,'walet_value':walet_value})


@login_required(login_url='/login/')
@user_passes_test(test_verification_application,login_url='/isell/home/')
def verification_request(request):
    if request.method == 'POST':

        user=request.user

        name = request.POST.get('name')
        ph_number = request.POST.get('ph_number')
        address_line_1 = request.POST.get('address_line_1')
        address_line_2 = request.POST.get('address_line_2')
        city = request.POST.get('city')
        state = request.POST.get('state')
        pincode = request.POST.get('pincode')
        purpose = request.POST.get('purpose')
        images = request.FILES.getlist('images')
        files = request.FILES.getlist('files')

        verification_process = seller_verification_process(seller=user)
        verification_process.name=name
        verification_process.phone_number=ph_number
        verification_process.address_line_1=address_line_1
        verification_process.address_line_2=address_line_2
        verification_process.city=city
        verification_process.state=state
        verification_process.pincode=pincode
        verification_process.purpose=purpose
        verification_process.images=[]
        verification_process.files=[]

        for each in images:
            fs = FileSystemStorage()
            fs.save('seller_images/'+each.name, each)
            verification_process.images.append('seller_images/'+each.name)

        for each in files:
            fs = FileSystemStorage()
            fs.save('seller_files/' + each.name, each)
            verification_process.files.append('seller_files/' + each.name)

        verification_process.save()
        user.verification_applied=True
        #________________del_________________
        # user.verification_status = True
        # sellers.objects.create(seller=user)
        # _________________________________
        user.save()

        return redirect(reverse('isell:isell_home'))

    else:

        return render(request,'verification_request.html')


@login_required(login_url='/login/')
@user_passes_test(test_verification,login_url='/isell/home/')
def add_products(request):
    user = request.user

    time_filter_dict = {'1':0, '3':1,'7':2,'30':3,'100':4}
    time_filter_list=["","","","","selected"]

    time_selected = "100"

    if request.method == 'POST':
        
        if request.POST.get('time') and (request.POST.get('time') in time_filter_dict.keys()):
            time_filter_list=["","","","",""]   
            time_filter_list[time_filter_dict[request.POST.get('time')]] = "selected"
            time_selected = request.POST.get('time')
        
        if request.POST.get('time')!="100":
            products = product.objects.filter(seller=sellers.objects.get(seller=user), date_of_post__gte=datetime.datetime.now()-datetime.timedelta(days=int(request.POST.get('time')))).order_by('-date_of_post') if len(product.objects.filter(seller=sellers.objects.get(seller=user), date_of_post__gte=datetime.datetime.now()-datetime.timedelta(days=int(request.POST.get('time'))))) > 0 else []
        else:
            products = product.objects.filter(seller=sellers.objects.get(seller=user)).order_by('-date_of_post') if len(product.objects.filter(seller=sellers.objects.get(seller=user))) > 0 else []
    else:
        products = product.objects.filter(seller=sellers.objects.get(seller=user)).order_by('-date_of_post') if len(product.objects.filter(seller=sellers.objects.get(seller=user))) > 0 else []


    count = 0
    seller = sellers.objects.get(seller=user)
    for each in seller.customization_requests_list:
        if each.accept_status == False and each.reject_status == False :
            count+=1

    walet_value = offlinewallet.objects.filter(user=lenders.objects.get(lender=request.user).lender)[0].price if offlinewallet.objects.filter(user=lenders.objects.get(lender=request.user).lender)[0].price else 0
    
    return render(request, 'add_products.html', {'products': products,'count':count,'date':datetime.datetime.now(),'time_filter_list':time_filter_list, 'time_selected': time_selected, 'walet_value': walet_value})



@login_required(login_url='/login/')
@user_passes_test(test_verification,login_url='/isell/home/')
def add_new_product(request):
    if request.method == 'POST':

        user = request.user
        data = json.loads(request.POST.get('data'))

        product_title=data['product_title']
        product_description= data['product_description']
        product_category_1 = data['product_category_1']
        product_category_2 =  data['product_category_2']
        product_details= data['product_types']
        additional_information =  data['additional_information']
        product_customisation_available = [data['customization_types']]
        additional_customization_information = data['additional_customization_information']
        date_of_post = datetime.datetime.now()

        for i in range(len(product_details)):

            new_product = product(seller=sellers.objects.get(seller=user))

            new_product.date_of_post = date_of_post

            new_product.product_title = product_title
            new_product.category_1 = product_category_1
            new_product.category_2 = product_category_2
            new_product.product_description = product_description

            new_product.product_name = product_details[i]['product_name']
            new_product.product_detail = product_details[i]['product_detail']
            new_product.product_color = product_details[i]['color']
            new_product.product_size = product_details[i]['size']
            new_product.product_price = float(product_details[i]['price'])
            new_product.product_discount = float(product_details[i]['disc_price'])
            new_product.product_final_price = round((float(product_details[i]['price']) - (
                    float(product_details[i]['price']) * float(product_details[i]['disc_price']) / 100)), 2)

            ex_keys = ['product_name', 'product_detail', 'color', 'size', 'price', 'disc_price']
            for each in ex_keys:
                del(product_details[i][each])

            new_product.product_remaining_details = [product_details[i]]
            new_product.additional_information = additional_information

            new_product.product_customisation_available = product_customisation_available
            new_product.additional_customization_information = additional_customization_information

            new_product.save()

            image_list = []
            images = request.FILES.getlist('product_type_images_' + str(i))
            print(images)
            for each in images:
                fs = FileSystemStorage()
                fs.save('seller_product_images/' + str(new_product.pk) + "/" + str(i) + "/" + each.name, each)
                image_list.append('seller_product_images/' + str(new_product.pk) + "/" + str(i) + "/" + each.name)

            new_product.images=image_list

            new_product.save()

        return redirect(reverse('isell:add_products'))

    else:

        count = 0
        seller = sellers.objects.get(seller=request.user)
        for each in seller.customization_requests_list:
            if each.accept_status == False and each.reject_status == False:
                count += 1

        walet_value = offlinewallet.objects.filter(user=lenders.objects.get(lender=request.user).lender)[0].price if offlinewallet.objects.filter(user=lenders.objects.get(lender=request.user).lender)[0].price else 0
    

        return render(request, 'add_product_form.html',{'count':count,'date':datetime.datetime.now(), 'categories' : categories, 'walet_value':walet_value})


@login_required(login_url='/login/')
@user_passes_test(test_verification,login_url='/isell/home/')
def edit_product(request):
    if request.method == 'POST':

        user = request.user
        data = json.loads(request.POST.get('data'))

        product_title = data['product_title']
        product_description = data['product_description']
        product_category_1 = data['product_category_1']
        product_category_2 = data['product_category_2']
        product_details = data['product_types']
        additional_information = data['additional_information']
        product_customisation_available = [data['customization_types']]
        additional_customization_information = data['additional_customization_information']
        date_of_post = datetime.datetime.now()

        for i in range(1):

            new_product = product.objects.get(pk=int(request.POST.get('product_pk')))

            new_product.date_of_post = date_of_post

            new_product.product_title = product_title
            new_product.category_1 = product_category_1
            new_product.category_2 = product_category_2
            new_product.product_description = product_description

            new_product.product_name = product_details[i]['product_name']
            new_product.product_detail = product_details[i]['product_detail']
            new_product.product_color = product_details[i]['color']
            new_product.product_size = product_details[i]['size']
            new_product.product_price = float(product_details[i]['price'])
            new_product.product_discount = float(product_details[i]['disc_price'])
            new_product.product_final_price = round((float(product_details[i]['price']) - (
                    float(product_details[i]['price']) * float(product_details[i]['disc_price']) / 100)), 2)

            ex_keys = ['product_name', 'product_detail', 'color', 'size', 'price', 'disc_price']
            for each in ex_keys:
                del (product_details[i][each])

            new_product.product_remaining_details = [product_details[i]]
            new_product.additional_information = additional_information

            new_product.product_customisation_available = product_customisation_available
            new_product.additional_customization_information = additional_customization_information

            new_product.save()

            image_list = []
            images = request.FILES.getlist('product_type_images_' + str(i))
            print(images)
            for each in images:
                fs = FileSystemStorage()
                fs.save('seller_product_images/' + str(new_product.pk) + "/" + str(i) + "/" + each.name, each)
                image_list.append('seller_product_images/' + str(new_product.pk) + "/" + str(i) + "/" + each.name)

            new_product.images = image_list

            new_product.save()

        return redirect(reverse('isell:add_products'))

    else:

        product_to_edit = product.objects.get(pk=int(request.GET.get('product_pk')))

        count = 0
        seller = sellers.objects.get(seller=request.user)
        for each in seller.customization_requests_list:
            if each.accept_status == False and each.reject_status == False:
                count += 1

        walet_value = offlinewallet.objects.filter(user=lenders.objects.get(lender=request.user).lender)[0].price if offlinewallet.objects.filter(user=lenders.objects.get(lender=request.user).lender)[0].price else 0

        return render(request, 'edit_product_form.html', {'product_to_edit': product_to_edit,'categories' : categories,'count': count, 'date': datetime.datetime.now(), 'walet_value':walet_value})



@login_required(login_url='/login/')
@user_passes_test(test_verification,login_url='/isell/home/')
def remove_product(request):

    product.objects.get(pk=int(request.GET.get('product_pk'))).delete()

    return redirect(reverse('isell:add_products'))



@login_required(login_url='/login/')
@user_passes_test(test_verification,login_url='/isell/home/')
def show_product(request):
    product_details = product.objects.filter(pk=int(request.GET.get('product_no')))
    if len(product_details)!=1:
        messages.error(request, 'Sorry!! You have already deleted that product ')
        return redirect(reverse('isell:add_products'))
    count = 0
    seller = sellers.objects.get(seller=request.user)
    for each in seller.customization_requests_list:
        if each.accept_status == False and each.reject_status == False:
            count += 1

    buyer_usernames=[]
    for each in product_details[0].ratings_comments:
        buyer_usernames.append(buyers.objects.get(pk=each.buyer_id).buyer.username)

    data=zip(buyer_usernames,product_details[0].ratings_comments)

    walet_value = offlinewallet.objects.filter(user=lenders.objects.get(lender=request.user).lender)[0].price if offlinewallet.objects.filter(user=lenders.objects.get(lender=request.user).lender)[0].price else 0

    return render(request, 'show_product.html', {'product_details': product_details[0],'data':data,'count': count, 'date': datetime.datetime.now(),'buyer_usernames':buyer_usernames, 'walet_value' : walet_value})

@login_required(login_url='/login/')
@user_passes_test(test_verification,login_url='/isell/home/')
def delivered_products(request):

    days_selected_time_filter = ""
    time_filter_dict = {'1':0, '3':1,'7':2,'30':3,'100':4}
    time_filter_list=["","","","","selected"]

    if request.method == 'POST':
        if request.POST.get('time') and (request.POST.get('time') in time_filter_dict.keys()):
            days_selected_time_filter = request.POST.get('time')
            time_filter_list=["","","","",""]   
            time_filter_list[time_filter_dict[request.POST.get('time')]] = "selected"

    seller = sellers.objects.get(seller=request.user)
    delivered_orders = []

    for each in seller.order_list:
        if each.delivery_status == True:
            if days_selected_time_filter != "" and days_selected_time_filter != "100":
                if (datetime.datetime.now() - each.date_of_order).days < int(days_selected_time_filter):
                    delivered_orders.append(each)
            else:     
                delivered_orders.append(each)
    count=0
    for each in seller.customization_requests_list:
        if each.accept_status == False and each.reject_status == False:
            count += 1

    walet_value = offlinewallet.objects.filter(user=lenders.objects.get(lender=request.user).lender)[0].price if offlinewallet.objects.filter(user=lenders.objects.get(lender=request.user).lender)[0].price else 0


    return render(request, 'delivered_products.html', {'delivered_orders': delivered_orders,'count': count, 'date': datetime.datetime.now(), 'time_filter_list':time_filter_list, 'days_selected_time_filter': days_selected_time_filter, 'walet_value' : walet_value})

@login_required(login_url='/login/')
@user_passes_test(test_verification,login_url='/isell/home/')
def applied_loans(request):

    days_selected_time_filter = ""
    time_filter_dict = {'1':0, '3':1,'7':2,'30':3,'100':4}
    time_filter_list=["","","","","selected"]

    if request.method == 'POST':
        if request.POST.get('time') and (request.POST.get('time') in time_filter_dict.keys()):
            days_selected_time_filter = request.POST.get('time')
            time_filter_list=["","","","",""]   
            time_filter_list[time_filter_dict[request.POST.get('time')]] = "selected"

    seller = sellers.objects.get(seller=request.user)
    applied_loans = []
    print("**********************************************")
    print(seller)
    for each in seller.loan_list:
        if days_selected_time_filter != "" and days_selected_time_filter != "100":
            if (datetime.datetime.now() - each.loan_applied_date).days < int(days_selected_time_filter):
                applied_loans.append(each)
        else:     
            applied_loans.append(each)

    count = 0
    for each in seller.customization_requests_list:
        if each.accept_status == False and each.reject_status == False:
            count += 1

    walet_value = offlinewallet.objects.filter(user=lenders.objects.get(lender=request.user).lender)[0].price if offlinewallet.objects.filter(user=lenders.objects.get(lender=request.user).lender)[0].price else 0

    return render(request, 'applied_loans.html', {'applied_loans': applied_loans,'count': count, 'date': datetime.datetime.now(), 'time_filter_list':time_filter_list, 'days_selected_time_filter':days_selected_time_filter, 'walet_value' : walet_value})


@login_required(login_url='/login/')
@user_passes_test(test_verification,login_url='/isell/home/')
def show_order(request):
    user=request.user
    seller = sellers.objects.get(seller=request.user)
    order_details=None
    for each in seller.order_list:
        if each.order_id==int(request.GET.get('order_pk')):
            order_details=each
    buyer=buyers.objects.get(id=order_details.buyer_id).buyer

    count = 0
    for each in seller.customization_requests_list:
        if each.accept_status == False and each.reject_status == False:
            count += 1

    walet_value = offlinewallet.objects.filter(user=lenders.objects.get(lender=request.user).lender)[0].price if offlinewallet.objects.filter(user=lenders.objects.get(lender=request.user).lender)[0].price else 0

    return render(request,'show_order.html',{'order_details':order_details,'buyer_name':buyer.username,'buyer_email':buyer.email,'buyer_mobile':buyer.mobile,'count': count, 'date': datetime.datetime.now(), 'walet_value': walet_value})

@login_required(login_url='/login/')
@user_passes_test(test_verification,login_url='/isell/home/')
def customization_requests(request):

    seller=sellers.objects.get(seller=request.user)

    if request.method == 'POST':

        if request.POST.get('req_code')=="1":
            data=[]
            for each in seller.customization_requests_list:
                if each.accept_status == False and each.reject_status == False:
                    data.append(each)

        elif request.POST.get('req_code')=="2":
            data=[]
            for each in seller.customization_requests_list:
                if each.accept_status == False and each.reject_status == True:
                    data.append(each)
        elif request.POST.get('req_code')=="3":
            data=[]
            for each in seller.customization_requests_list:
                if each.accept_status == True and each.reject_status == False:
                    data.append(each)
        else:
            data = seller.customization_requests_list
    else:
        data = seller.customization_requests_list

    count = 0

    for each in seller.customization_requests_list:
        if each.accept_status == False and each.reject_status == False:
            count += 1

    walet_value = offlinewallet.objects.filter(user=lenders.objects.get(lender=request.user).lender)[0].price if offlinewallet.objects.filter(user=lenders.objects.get(lender=request.user).lender)[0].price else 0


    return render(request, 'customization_requests.html',{'data':data,'req_code':request.POST.get('req_code'),'count':count,'date':datetime.datetime.now(), 'walet_value':walet_value})

@login_required(login_url='/login/')
@user_passes_test(test_verification,login_url='/isell/home/')
def accept_reject_customization_requests(request):
    if request.method=='POST':
        cust = customization.objects.get(pk=int(request.POST.get('cust_id')))
        if request.POST.get('value')=='0':
            cust.accept_status=False
            cust.reject_status=True
            cust.accepted_details=[None]
            cust.save()
        elif request.POST.get('value')=='1':
            cust.accept_status=True
            cust.reject_status=False
            if len(cust.accepted_details)==0:
                cust.accepted_details=cust.customization_details
            cust.save()
    return redirect('http://127.0.0.1:8000/isell/customization_requests/')


@login_required(login_url='/login/')
@user_passes_test(test_verification,login_url='/isell/home/')
def reply_customization_requests(request):
    if request.method == 'POST':
        cust = customization.objects.get(pk=int(request.POST.get('cust_id')))
        accepted_values={}
        for i in range(len(cust.customization_details[0])):
            if request.POST.get('key_val_'+str(i)) != None:
                accepted_values[request.POST.get('key_val_'+str(i))]=cust.customization_details[0][request.POST.get('key_val_'+str(i))]
        if accepted_values!={}:
            cust.accepted_details=[accepted_values]
            cust.accept_status=True
            cust.reject_status=False
        else:
            cust.accepted_details = [None]
            cust.accept_status = False
            cust.reject_status = True
        cust.save()
    return redirect('http://127.0.0.1:8000/isell/customization_requests/')



@login_required(login_url='/login/')
@user_passes_test(test_verification,login_url='/isell/home/')
def write_reply(request):

    ratings_and_comments_=ratings_comments.objects.get(pk=int(request.GET.get('rc_id')))
    ratings_and_comments_.reply=request.GET.get('my_reply')
    ratings_and_comments_.reply_timestamp=datetime.datetime.now()
    ratings_and_comments_.save()

    product_details = product.objects.filter(pk=ratings_and_comments_.product.id)
    if len(product_details) != 1:
        messages.error(request, 'Sorry!! You have already deleted that product ')
        return redirect(reverse('isell:add_products'))
    count = 0
    seller = sellers.objects.get(seller=request.user)
    for each in seller.customization_requests_list:
        if each.accept_status == False and each.reject_status == False:
            count += 1

    buyer_usernames = []
    for each in product_details[0].ratings_comments:
        buyer_usernames.append(buyers.objects.get(pk=each.buyer_id).buyer.username)

    data = zip(buyer_usernames, product_details[0].ratings_comments)

    walet_value = offlinewallet.objects.filter(user=lenders.objects.get(lender=request.user).lender)[0].price if offlinewallet.objects.filter(user=lenders.objects.get(lender=request.user).lender)[0].price else 0

    return render(request, 'show_product.html',
                  {'product_details': product_details[0], 'data': data, 'count': count, 'date': datetime.datetime.now(),
                   'buyer_usernames': buyer_usernames, 'walet_value' : walet_value})


@login_required(login_url='/login/')
@user_passes_test(test_verification,login_url='/isell/home/')
def loan_details(request):
    user = request.user
    seller = sellers.objects.get(seller=request.user)
    order_details = None
    for each in seller.order_list:
        if each.order_id == int(request.GET.get('order_pk')):
            order_details = each
    buyer = buyers.objects.get(id=order_details.buyer_id).buyer

    count = 0
    for each in seller.customization_requests_list:
        if each.accept_status == False and each.reject_status == False:
            count += 1

    loan_details=loan.objects.get(order=order.objects.get(pk=int(request.GET.get('order_pk'))))

    walet_value = offlinewallet.objects.filter(user=lenders.objects.get(lender=request.user).lender)[0].price if offlinewallet.objects.filter(user=lenders.objects.get(lender=request.user).lender)[0].price else 0

    return render(request, 'show_loan_details.html',
                  {'order_details': order_details, 'buyer_name': buyer.username, 'buyer_email': buyer.email, 'walet_value' : walet_value,
                   'buyer_mobile': buyer.mobile, 'count': count, 'date': datetime.datetime.now(),'loan_details':loan_details})

from ilend.views import loan_taken

@login_required(login_url='/login/')
@user_passes_test(test_verification,login_url='/isell/home/')
def apply_loan(request):
    user = request.user
    seller_details = sellers.objects.filter(seller=request.user)[0]

    orders = seller_details.order_list
    pending_orders = []

    for each in orders:
        if each.delivery_status == False:
            pending_orders.append(each)

    if request.method == 'POST':
        order_id = int(request.POST.get('order_pk'))
        amount = int(request.POST.get('amount'))
        (acceptance, amount) = loan_taken(order_id, amount, True)


    else:
        order_id = int(request.GET.get('order_pk'))
        print(loan_taken(order_id, 0, False))
        (acceptance, amount) = loan_taken(order_id, 0, False)


    count = 0
    try:
        for each in seller_details.customization_requests_list:
            if each.accept_status == False and each.reject_status == False:
                count += 1
    except:
        pass

    walet_value = offlinewallet.objects.filter(user=lenders.objects.get(lender=request.user).lender)[0].price if offlinewallet.objects.filter(user=lenders.objects.get(lender=request.user).lender)[0].price else 0

    return render(request, 'index3.html',
                  {'pending_orders': pending_orders, 'order_id': order_id, 'acceptance': acceptance, 'amount': amount, 'count': count, 'date': datetime.datetime.now(), 'walet_value':walet_value})




