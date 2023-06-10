from django.http import HttpResponse
from django.shortcuts import redirect
from .models import Products
from account.models import MemberShipType
from django.shortcuts import render
from django.urls import reverse
from django.contrib import messages

def MemberShipTypeList(request):
    slug1 = "Users"
    create_link_name = reverse("MemberShipCreate")
    all_data = MemberShipType.objects.all()

    data = {'slug1':slug1,'create_link_name':create_link_name, 'membership_types':all_data}
    return render(request , "admin/membership/membership-list.html",data)

def MemberShipCreate(request,id=None):
    create_link_name = reverse("MemberShipCreate")
    if id==None:
        slug1 = "membership-type-create" 
    else:
        slug1 = "membership-type-update" 
    action = "MemberShipStore"
    #Fetching the data of particular ID
    get_data = None
    if id:
        action = "MemberShipStore"
        get_data = MemberShipType.objects.get(id=id)  

    data = {'slug1':slug1,'create':False,'create_link_name':create_link_name,'id_data':get_data, 'action':action}
    return render(request, "admin/membership/membership-form.html",data)

def MemberShipStore(request,id=None):
    # return HttpResponse(request.POST.items())
    if request.POST['discount'] == '':
        discount = 0
    else:
        discount = request.POST['discount']

    if request.POST['discount_shipping_apply'] == "1":
        is_shipping_free = request.POST['is_shipping_free']
    else:
        is_shipping_free = "0"

    if request.POST:
        name = request.POST['name']
        discount_shipping_apply = request.POST['discount_shipping_apply']

        obj = MemberShipType.objects.get(id=id)
        obj.name=name
        obj.discount_shipping_apply=discount_shipping_apply
        obj.is_shipping_free=is_shipping_free
        obj.discount=discount
        obj.save()
        if obj:
            messages.success(request,"Inserted successfully !!!")
        else:
            messages.error(request,"Failed to create Membership !!!")
        return redirect(MemberShipTypeList)

def MemberShipDelete(request,id):
    return HttpResponse(id)
    try:
        user = MemberShipType.objects.get(id=id).delete()
        messages.success(request, 'User deleted sucessfully!!!.')
        return redirect(MemberShipTypeList)
    except:
        messages.info(request,"foreign key constraint fails CONSTRAINT error")
        return redirect(MemberShipTypeList)


def MemberShipTypeUser(request):
    slug1 = "Users"
    create_link_name = reverse("UserCreate")
    all_data = MemberShipType.objects.all()

    data = {'slug1':slug1,'create':True,'create_link_name':create_link_name, 'users':all_data}
    return render(request , "admin/membership/membership-type-user.html",data)

def InsertMemberShip(request):
    membership_obj =  Products.membership_type
    for i in membership_obj:
        code_name = i[0]
        name = i[1]
        id = i[2]
        data = {
            'code_name' : code_name,
            'name' : name,
        }
        obj,create = MemberShipType.objects.update_or_create(id=id,defaults=data)
        if(create):
            print(code_name + " : created ")
        else:
            print(code_name+" : failed to create ")

    return HttpResponse("data inserted successfully !!!")

