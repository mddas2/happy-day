from django.http import HttpResponse
from django.contrib.auth import authenticate,login,logout
from axes.models import AccessAttempt
from django.shortcuts import render,redirect
from django.contrib import messages
from django.conf import settings


def Login(request):   
    data = {}
    login_attempt_left = 20
    if request.POST:
        # return HttpResponse(request.POST)

        email = request.POST['email']
        password =  request.POST['password']
        user = authenticate(request=request,username=email, password=password)
        if user is not None:
            login(request,user,backend='django.contrib.auth.backends.ModelBackend') 
            return redirect('website.index') 
        else:
            try:
                user_login_attempt = AccessAttempt.objects.filter(username=email).first().failures_since_start
                login_attempt_left = settings.AXES_FAILURE_LIMIT-user_login_attempt
            except:
                login_attempt_left =  settings.AXES_FAILURE_LIMIT

            # return HttpResponse(login_attempt_left)
            messages.error(request, "incorrect user or password")

    return render(request, 'client_dashboard/login.html',data)

def Logout(request):
    logout(request)
    return redirect('Login') 

def ViewOrderHistory(request):
    data = {}
    return render(request,'client_dashboard/order_history.html',data)

def ViewWishList(request):
    data = {}
    return render(request,'client_dashboard/wish_list.html',data)

def Signup(request):
    if request.POST:
        return HttpResponse("this is user create")
    return render(request, 'client_dashboard/signup.html')

def Profile(request):
    if request.POST:
        return HttpResponse("this is user create")
    return render(request, 'client_dashboard/profile.html')