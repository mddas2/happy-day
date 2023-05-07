from ast import Return
from django.http import HttpResponse
from django.urls import reverse
from root.models import *
from django.shortcuts import render
from django.shortcuts import redirect
import random
from django.core.paginator import Paginator
from datetime import datetime, timedelta

def CategoryAction(request,page_type,page_detail,c_id=None):
    # return HttpResponse(request.GET['product'])
    menus = Navigation.objects.filter(parent_page_id=0, status=1).order_by('position')
    page_types = PageType.objects.all()
    customers = HomeNavigation.objects.filter(page_type='normal').order_by('-updated_at')[:3]
    Categories = Navigation.objects.filter(page_type='sale_group').order_by('position')

    # nav = Navigation.objects.filter(id=page_detail.first().id)
    # product = nav.product.all()
    #page_detail.first().name
    if request.GET:
        if request.GET['product'] == 'deal_of_the_week':
            last_week = datetime.now() - timedelta(days=7)
            all_product = Products.objects.filter(status=1).filter(updated_at__gte=last_week)
        elif request.GET['product'] == 'popular':
            all_product = Products.objects.filter(status=1).order_by('-most_ordered') 
        elif request.GET['product'] == 'door_phone':
            all_product = Products.objects.filter(status=1).filter(vendor="door_phone").order_by('-updated_at')
        else:
            all_product = Products.objects.filter(status=1).filter(vendor="camera").order_by('-updated_at')
    else:
        all_product = Products.objects.filter(status=1).order_by('-updated_at')  
    # team = Team.objects.all()
    blog = Blog.objects.filter(status=1).order_by('-updated_at')[:6]
    global_data = GlobalSettings.objects.first()
    wishvalue = Wishlist.objects.filter(temp_id=c_id,ishere=True)
    cartvalue = Wishlist.objects.filter(temp_id=c_id,ishere=False)
    wishvalue = len(wishvalue)
    cartvalue = len(cartvalue)

    product = None
    about = None
    for i in page_types:      
        if page_type==i.page_name :   
            if page_type == 'normal':
                # return HttpResponse("normal")
                about = Navigation.objects.filter(page_type='normal').all().first()
                # return HttpResponse(about.name)
            # if page_type == 'product':
            #     return HttpResponse("product")
            # if page_type == 'sale':
            product = Paginator(all_product, 16)
            page_number = request.GET.get('page')
            product = product.get_page(page_number)
            # if page_type == 'blog':
            #     return HttpResponse("blog")
            if page_type == 'group':
                about = "yes_i_am"
                # return HttpResponse(about) 
            # return HttpResponse(page_detail.name)
            data = {'menus':menus,'global_data':global_data,'all_product':all_product,'product':product,'about':about,'customers':customers,'Categories':Categories,
                    'team':'team','page_detail':page_detail,'blog':blog, 'c_id':c_id, 'wishvalue':wishvalue, 'cartvalue':cartvalue
                }
            if page_type == 'product':
                data['page'] = "product"
            return render(request,'main/'+page_type+'.html',data)

      
    return redirect('website.index')
            # return reverse("SubNavigationCreate", args=[id])


def SubcategoryAction(request,page_type,page_detail,c_id=None,submenu=None):
    menus = Navigation.objects.filter(parent_page_id=0, status=1).order_by('position')
    breadcom = menus.first().caption
    page_types = PageType.objects.all()
    Categories = Navigation.objects.filter(page_type='sale_group').order_by('position')
    # nav = Navigation.objects.filter(id=page_detail.first().id)
    # product = nav.product.all()
    #page_detail.first().name
    # team = Team.objects.all()
    # blog = Blog.objects.filter(status=1)
    global_data = GlobalSettings.objects.first()

    wishvalue = Wishlist.objects.filter(temp_id=c_id,ishere=True)
    cartvalue = Wishlist.objects.filter(temp_id=c_id,ishere=False)
    wishvalue = len(wishvalue)
    cartvalue = len(cartvalue)

    product = None
    all_product = None

    for i in page_types:      
        if page_type==i.page_name :  
            # if page_type == 'normal':
            #     return HttpResponse("normal")
            # if page_type == 'product':
            #     return HttpResponse("product")
            if page_type == 'sale':
                nav_id = Navigation.objects.filter(name = submenu).get()
                all_product = Products.objects.filter(category_id = nav_id.id, status=1 )  
                # return HttpResponse(print (all_product))
                if all_product != None:
                    product = Paginator(all_product, 9)
                    page_number = request.GET.get('page')
                    product = product.get_page(page_number)
            # if page_type == 'blog':
            #     return HttpResponse("blog")
            # if page_type == 'contact':
            #     return HttpResponse("contact")
            data = {'menus':menus,'global_data':global_data,'all_product':all_product,'product':product,'Categories':Categories,
                    'team':'team','page_detail':page_detail,'blog':'blog', 'c_id':c_id, 'wishvalue':wishvalue, 'cartvalue':cartvalue
                } 
            return render(request,'main/'+page_type+'.html',data)