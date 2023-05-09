from django.contrib import messages
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.shortcuts import render
from root.models import *
from account.models import *
from website.includes.Action import *
from datetime import datetime, timedelta


#Mail
import smtplib
from string import Template
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.image import MIMEImage
import os
from pathlib import Path
BASE_DIR = Path(__file__).resolve(strict=True).parent.parent


# Create your views here.
def index(request):        
        # return render(request, 'index.html')
        menus = Navigation.objects.filter(parent_page_id=0, status=1).order_by('position')
        blog = Blog.objects.filter(status=1).order_by('-updated_at')[:3]
        sliders = HomeNavigation.objects.filter(page_type='sale')
        contact_section = HomeNavigation.objects.filter(page_type='contact').all().first()
        clients = HomeNavigation.objects.filter(page_type='blog')
        customers = HomeNavigation.objects.filter(page_type='normal').order_by('-updated_at')[:3]
        happy_customer = HomeNavigation.objects.filter(name="Happy_Customers").order_by('-updated_at').first().childs.all()
        
        Categories = Navigation.objects.filter(parent_id=3).order_by('position')[:7]

        # sub_category = Navigation.objects.filter(page_type="sale").order_by('position')
        # return HttpResponse(Categories)
        clientsobj = HomeNavigation.objects.filter(name='clients').all().first()
        clientschild = []
        if clientsobj:
                clientschild = clientsobj.childs.all()
        pemplateobj = HomeNavigation.objects.filter(name='pemplate').all().first()
        pemplatechild = []
        if pemplateobj:
                pemplatechild = pemplateobj.childs.all()
        ftn = request.GET.get('ftn')
        if ftn:
                product = Products.objects.filter(ftn=ftn)  
        else:
                all_product = Products.objects.filter(status=1).order_by('-created_at')
        
        # most_ordered = Products.objects.filter(status=1).order_by('-most_ordered')[:12]  # #

        best_selling = Products.objects.filter(status=1).order_by('-discount')[:6]
        latest_product = Products.objects.filter(status=1).order_by('-updated_at')[:12]
        # special_deals = Products.objects.filter(status=1).order_by('-most_ordered','-updated_at')[:12]
        camera = Products.objects.filter(status=1).filter(vendor="camera").order_by('-updated_at')[:12] # #
        door_phone = Products.objects.filter(status=1).filter(vendor="door_phone").order_by('-updated_at') # #

        last_week = datetime.now() - timedelta(days=7)
        deal_of_the_week = Products.objects.filter(status=1).filter(updated_at__gte=last_week)[:20] # #

        product = Paginator(all_product, 12)
        page_number = request.GET.get('page')
        product = product.get_page(page_number) # #

        global_data = GlobalSettings.objects.first()
        data = {
            'page':"index",
            'global_data':global_data,
            'camera':camera,
            'door_phone':door_phone,
            'deal_of_the_week':deal_of_the_week,
            'latest_product':latest_product,
            'best_selling':best_selling,
            'categories':Categories,
            'page_number':page_number,
            'customers':customers,
            'clients':clients,
            'contact_section':contact_section,
            'menus':menus,
            'blog':blog,
            'product':product,
            'sliders':sliders,
            'clientschild':clientschild,
            'pemplatechild':pemplatechild,
            'happy_customer' : happy_customer,
        }
        try:
            temp_id = request.user.c_id
            c_id = None
        except:
            try: 
                c_id = request.COOKIES['c_id']
            except:
                c_id = None
            temp_id = None

        if c_id:
            cartvalue = Wishlist.objects.filter(temp_id=c_id,ishere=False)
            wishvalue = Wishlist.objects.filter(temp_id=c_id,ishere=True)
            cartvalue = len(cartvalue)
            wishvalue = len(wishvalue)
            data['c_id'] = c_id
            data['cartvalue'] = cartvalue
            data['wishvalue'] = wishvalue
            return render(request, 'index.html',data)
        else:  
            if temp_id:  
                try: 
                    c_id = request.COOKIES['c_id']
                except:
                    c_id = None

                if c_id:
                    Wishlist.objects.filter(temp_id=c_id).update(temp_id=temp_id)
                
                cartvalue = Wishlist.objects.filter(temp_id=temp_id,ishere=False)
                wishvalue = Wishlist.objects.filter(temp_id=temp_id,ishere=True)
                cartvalue = len(cartvalue)
                wishvalue = len(wishvalue)
                data['cartvalue'] = cartvalue
                data['wishvalue'] = wishvalue
                data['c_id'] = temp_id

                a = render(request, 'index.html',data)
                a.set_cookie(key="c_id", value=temp_id,max_age=100000000)
                return a
            else:
                rand_num = random.randint(100000,1000000)
                data['c_id'] = rand_num

                a = render(request, 'index.html',data)
                a.set_cookie(key="c_id", value=rand_num,max_age=100000000)
                return a
def Category(request, menu):
    try:
        c_id = request.COOKIES['c_id']
    except:
        return redirect('website.index')
    page_detail = Navigation.objects.filter(name=menu).first() ##to display contants
    if Navigation.objects.filter(name=menu).first():
        page_type = Navigation.objects.filter(name=menu).first().page_type
    else:
        page_type = None
    # return HttpResponse(page_type)
    return CategoryAction(request,page_type,page_detail,c_id)   

def SubCategory(request, menu , submenu ):
    if menu=='admin':
        return redirect('/') #if user(client) input admin as menu then redirect to home
    else:
        if Navigation.objects.filter(name=submenu).first()==None: #if user input rough url then redirect to home
            return redirect('/')
    try:
        c_id = request.COOKIES['c_id']
    except:
        return redirect('website.index')
    page_detail = Navigation.objects.filter(name=submenu).first()
    if Navigation.objects.filter(name=submenu).first():
        page_type = Navigation.objects.filter(name=submenu).first().page_type
    else:
        page_type = None
    page_type = Navigation.objects.filter(name=submenu).first().page_type
    return SubcategoryAction(request,page_type,page_detail,c_id,submenu)   
    # return SubcategoryAction(request,page_type,menu,submenu)

def ProductDetail(request,id):
    try:
        c_id = request.COOKIES['c_id']
    except:
        return redirect('website.index')
    menus = Navigation.objects.filter(parent_page_id=0,status=1).order_by('position')
    product = Products.objects.get(id=id,status=1) 
    
    customers = HomeNavigation.objects.filter(page_type='normal').order_by('-updated_at')[:3]
    best_price = Products.objects.filter(status=1).order_by('-discount')[:3]
    Categories = Navigation.objects.filter(page_type='sale_group').order_by('position')


    sizes = product.size.split(',')
    colors = product.color.split(',')
    related_product = Products.objects.filter(category_id=product.category_id,status=1).order_by('-updated_at')
    # print(product.category_id)
    global_data = GlobalSettings.objects.first()

    wishvalue = Wishlist.objects.filter(temp_id=c_id,ishere=True)
    cartvalue = Wishlist.objects.filter(temp_id=c_id,ishere=False)
    wishvalue = len(wishvalue)
    cartvalue = len(cartvalue)


    data = {'product':product,'global_data':global_data,'customers':customers,'Categories':Categories,'wishvalue':wishvalue, 'cartvalue':cartvalue, 'best_price':best_price,'menus':menus,'c_id':c_id,'related_product':related_product,'sizes':sizes,'colors':colors}
    return render(request, 'main/product-details.html',data)

def BlogDetail(request,id):
    try:
        c_id = request.COOKIES['c_id']
    except:
        return redirect('website.index')
    menus = Navigation.objects.filter(parent_page_id=0,status=1).order_by('position')
    blog = Blog.objects.get(id=id) 
    global_data = GlobalSettings.objects.first()
    wishvalue = Wishlist.objects.filter(temp_id=c_id,ishere=True)
    cartvalue = Wishlist.objects.filter(temp_id=c_id,ishere=False)
    wishvalue = len(wishvalue)
    cartvalue = len(cartvalue)
    data = {'blog_detail':blog,'global_data':global_data,'menus':menus,'wishvalue':wishvalue, 'cartvalue':cartvalue }
    return render(request, 'main/normal.html',data)

def WishList(request, p_id=None ,c_id=None):
    try:
        c_id = request.COOKIES['c_id']
    except:
        return redirect('website.index')
    if p_id and c_id :
        if request.POST:
            data = {
                'size' : request.POST['size'],
                'quantity' : request.POST['number'],
                'color' : request.POST['color'], 
                'product_id' : p_id,
                'temp_id' : c_id
            }
            addingwishes = Wishlist.objects.update_or_create(temp_id=c_id,product_id=p_id,ishere=True,defaults=data)
            return redirect('WishList')
        else:
            data = {
                'product_id' : p_id,
                'temp_id' : c_id,
                'quantity' : 1,
            }
            addingwishes = Wishlist.objects.update_or_create(temp_id=c_id,product_id=p_id,ishere=True,defaults=data)
            return redirect(request.META.get('HTTP_REFERER'))
    menus = Navigation.objects.filter(parent_page_id=0,status=1).order_by('position')
    wishlist = Wishlist.objects.filter(temp_id=c_id,ishere=True)
    global_data = GlobalSettings.objects.first()
    wishvalue = Wishlist.objects.filter(temp_id=c_id,ishere=True)
    cartvalue = Wishlist.objects.filter(temp_id=c_id,ishere=False)
    data = {'menus':menus,'global_data':global_data ,'wishlist':wishlist,'c_id':c_id,}
    data['wishvalue'] = len(wishvalue)
    data['cartvalue'] = len(cartvalue)
    return render(request, 'main/wish-list.html', data)

def Cart(request, p_id=None ,c_id=None):
    try:
        c_id = request.COOKIES['c_id']
    except:
        return redirect('website.index')
    if p_id and c_id :
        if request.POST: 
            data = {
                # 'size' : request.POST['size'],/
                'quantity' :  request.POST['number'],
                # 'color' : request.POST['color'], 
                'product_id' : p_id,
                'temp_id' : c_id,
                'user_id' : request.user.id,
                'ishere' : False
            }
            # prod = Products.objects.filter(id=p_id).get()
            # if prod.quantity < int(request.POST['number']):
            #     messages.warning(request,"Given Quantity Not available.") 
            #     data['quantity'] = prod.quantity
            # else:
            #     data['quantity'] =  request.POST['number']
            addingwishes = Wishlist.objects.update_or_create(temp_id=c_id,product_id=p_id,ishere=False,defaults=data)
            return redirect('Cart')
        else:
            data = {
                'product_id' : p_id,
                'temp_id' : c_id,
                'ishere' : False,
                'quantity' :  1,
            }
            # prod = Products.objects.filter(id=p_id).get()
            # if prod.quantity < int(p_id):
            #     messages.warning(request,"Given Quantity Not available.") 
            #     data['quantity'] = prod.quantity
            # else:
            #     data['quantity'] =  p_id
            addingwishes = Wishlist.objects.update_or_create(temp_id=c_id,product_id=p_id,ishere=False,defaults=data)
            deleteifcolide = Wishlist.objects.filter(temp_id=c_id,product_id=p_id,ishere=True)
            deleteifcolide.delete()
            return redirect(request.META.get('HTTP_REFERER'))
    menus = Navigation.objects.filter(parent_page_id=0,status=1).order_by('position')
    wishlist = Wishlist.objects.filter(temp_id=c_id,ishere=False)
    global_data = GlobalSettings.objects.first()
    Categories = Navigation.objects.filter(page_type='sale_group').order_by('position')

    data = {'menus':menus,'global_data':global_data, 'wishlist':wishlist,'c_id':c_id,'Categories':Categories}
    wishvalue = Wishlist.objects.filter(temp_id=c_id,ishere=True)
    cartvalue = Wishlist.objects.filter(temp_id=c_id,ishere=False)
    data['wishvalue'] = len(wishvalue)
    data['cartvalue'] = len(cartvalue)
    return render(request, 'main/cart.html', data)

def cartQuantityUpdate(request):
    try:
        c_id = request.COOKIES['c_id']
    except:
        return redirect('website.index')
    Wishlist.objects.filter(id=request.GET.get('id')).update(quantity= request.GET.get('quantity'))
    return HttpResponse("Successfully Updated!")


@login_required(login_url=settings.CLIENT_LOGIN_URL)
def WishListDelete(request, p_id, pk, next):
    udata = Wishlist.objects.filter(temp_id=pk,product_id=p_id)
    udata.delete()
    if next=="cart":
        return redirect('Cart')
    elif next=="wish":
        return redirect('WishList')
    else:
        return redirect('website.index')


def read_template(filename):
    with open(filename, 'r') as template_file:
        template_file_content = template_file.read()
    return template_file_content

 # ishere field [ 1(TRUE) =>wishlist) ], [ 0(false) => cart)]  , 2=> order
@login_required(login_url=settings.CLIENT_LOGIN_URL)
def CheckOut(request):
    try:
        c_id = request.COOKIES['c_id']
    except:
        return redirect('index_ecom')
    if Wishlist.objects.filter(temp_id=c_id,ishere=False):
        if request.POST:        
            for i in Wishlist.objects.filter(temp_id=c_id,ishere=False) :
                shipping_data = {
                    'user_id' : request.user.id,
                    'name'    : request.POST['name'],
                    'phone'   : request.POST['phone'],
                    'email'   : request.POST['email'],
                    'shpping_address' : request.POST['address'],
                }
                ship =  Shipping.objects.create(**shipping_data)
                data = {
                    'user_detail' : request.POST['name'],
                    'phone' :  request.POST['phone'],
                    'shipping_address' : request.POST['address'], 
                    'user_id' : request.user.id, 
                    'product_id' : i.product_id,
                    'product_details' : i.quantity,
                    'get_shipping_address_id' : ship.id,
                }
             
                Order.objects.create(**data)
                prod = Products.objects.filter(id=i.product_id).get()
                if(prod.quantity > i.quantity):
                    temp = prod.quantity - i.quantity
                    if(temp >= 0):
                        prod.quantity = temp
                        prod.save()
                # Order.objects.update_or_create(product_id=data['product_id'],user_id=c_id,defaults=data)
            messages.info(request,"Successfully Orderd ! We will contact you very Soon. ")
            Wishlist.objects.filter(temp_id=c_id,ishere=False).update(ishere=2)
            return redirect('Cart')            
        menus = Navigation.objects.filter(parent_page_id=0).order_by('position')
        global_data = GlobalSettings.objects.first()
        Categories = Navigation.objects.filter(page_type='sale_group').order_by('position')
 
        data = {'global_data':global_data,'menus':menus,'Categories':Categories}  
        wishvalue = Wishlist.objects.filter(temp_id=c_id,ishere=True)
        cartvalue = Wishlist.objects.filter(temp_id=c_id,ishere=False)
        data['wishvalue'] = len(wishvalue)
        data['cartvalue'] = len(cartvalue)
        return render(request, 'main/checkout.html', data)

    else:
        messages.error(request,"Please add to Cart. Before Checkout")
        return redirect('Cart')

def Custom(request):
    try:
        c_id = request.COOKIES['c_id']
    except:
        return redirect('website.index')
    
    if request.POST: 

        MY_ADDRESS = 'fenfit@fenfitnepal.com'
        PASSWORD = 'fenfit@devraj'
        user_info = {
            'name'    : request.POST['name'],
            'phone'   : request.POST['phone'],
            'email'   : request.POST['email'],
            'shpping_address' : request.POST['address'],
            'billing_address' : request.POST['baddress'],
            'current_address' : request.POST['caddress'],
            'product_name'    : request.POST['product_name'],
            'size'   : request.POST['size'],
            'color'   : request.POST['color'],
            'quantity'   : request.POST['number'],
        }
        get_data = GlobalSettings.objects.only('configure_email').first()        
        emails = get_data.configure_email

        # html = html.replace('{{names}}',names)
        try:
            s = smtplib.SMTP(host='mail.fenfitnepal.com', port=587)
            s.starttls()
            s.login(MY_ADDRESS, PASSWORD)
        except:
            messages.info(request,"Connecting To Mail Server Failed !!!")
            return redirect('website.index') 

        html = read_template(os.path.join(BASE_DIR ,'website/templates/main/custom-messages.html'))
        msg = MIMEMultipart()       # create a message
        msg['From']=MY_ADDRESS
        msg['To']=emails
        msg['Subject']="Order Details"

        # This example assumes the image is in the current directory
        fp = open(os.path.join(BASE_DIR ,'website/static/assets/images/logo.png'), 'rb')
        msgImage = MIMEImage(fp.read())
        fp.close()
        
        html = html.replace("{{product_name}}",str(user_info['product_name']))
        html = html.replace("{{size}}",str(user_info['size']))
        html = html.replace("{{color}}",str(user_info['color'])) 
        html = html.replace("{{quantity}}",str(user_info['quantity'])) 
        html = html.replace("{{Name}}",str(user_info['name']))
        html = html.replace("{{Email}}",str(user_info['email']))
        html = html.replace("{{Phone_Number}}",str(user_info['phone']))
        html = html.replace("{{Shipping_Address}}",str(user_info['shpping_address']))
        html = html.replace("{{Billing_Address}}",str(user_info['billing_address']))
        html = html.replace("{{Current_Address}}",str(user_info['current_address']))



        # Define the image's ID as referenced above
        msgImage.add_header('Content-ID', '<image0>')
        msg.attach(msgImage)     
       
        msg.attach(MIMEText(html, 'html'))
        s.send_message(msg)
        del msg
        # Terminate the SMTP session and close the connection
        s.quit()

        messages.info(request,"Successfully Orderd ! We will contact you very Soon. ")
        return redirect('website.index')            

    else:
        messages.error(request,"Please Try Again !!!")
        return redirect('website.index')

@login_required(login_url=settings.CLIENT_LOGIN_URL)
def Contactus(request):
    if request.POST:
        data = {
            'name' : request.POST['name'],
            'email' :  request.POST['email'],
            'subject' : request.POST['subject'], 
            'message' : request.POST['message'], 
        }
        if 'p_id' in request.POST:
            products = Products.objects.get(id=request.POST['p_id'])
            products.star = int(products.star) + 1
            products.save()

            data_review = {
                'star' : request.POST['stars'],
                'product_id' : request.POST['p_id'],
                'user_id' : request.user.id,
            }
            Review.objects.update_or_create(user_id=request.user.id,product_id=request.POST['p_id'],defaults=data_review)

        # return HttpResponse(request.POST['subject'])
        ContactUs.objects.create(**data)
        messages.error(request,"You Message has been Sent Successfully !")
        return redirect('/about-us')

@login_required(login_url=settings.CLIENT_LOGIN_URL)
def RateProduct(request):
    data = {
        'name' : request.POST['name'],
        'email' :  request.POST['email'],
        'subject' : request.POST['subject'], 
        'message' : request.POST['message'], 
    }

    products = Products.objects.get(id=request.POST['p_id'])
    products.star = int(products.star) + 1
    products.save()

    data_review = {
        'star' : request.POST['stars'],
        'product_id' : request.POST['p_id'],
        'user_id' : request.user.id,
    }
    Review.objects.update_or_create(user_id=request.user.id,product_id=request.POST['p_id'],defaults=data_review)

    # return HttpResponse(request.POST['subject'])
    ContactUs.objects.create(**data)
    messages.error(request,"You Message has been Sent Successfully !")
    return redirect('/about-us')


def Login(request):
    return render(request, 'main/login.html')


def Signup(request):
    return render(request, 'main/register.html')


      
   