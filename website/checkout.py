from django.contrib.auth.decorators import login_required
from django.conf import settings
import json
from django.http import HttpResponse
from django.shortcuts import render

@login_required(login_url=settings.CLIENT_LOGIN_URL)
def CheckOut(request):
    from .my_form import CheckOutForm
    cart_data_str = request.COOKIES.get('cart')
    cart_data = json.loads(cart_data_str) if cart_data_str else []
    if request.POST:
        form = CheckOutForm(request.POST)
        if form.is_valid():
            form.save()            
            return HttpResponse("cart going to add")  
          
    else:
        form = CheckOutForm()
    data = {
         'cart_data':cart_data,
         'form':form
    }
    return render(request, 'main/checkout.html',data)