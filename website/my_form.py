from django import forms
from account.models import CustomUser
from root.models import Shipping,Order

class CheckOutForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
        user = self.request.user if self.request and self.request.user.is_authenticated else None       
        if user and user.is_authenticated:
            self.fields['firstname'].initial = user.first_name
            self.fields['lastname'].initial = user.last_name
            self.fields['email'].initial = user.email
            self.fields['phone'].initial = user.phone

            shipping_address_obj =  user.shipping.all()
            if shipping_address_obj.count()>0:
                shipping_address_obj = shipping_address_obj.last()                  
                self.fields['company'].initial = shipping_address_obj.company_name
                self.fields['address_1'].initial = shipping_address_obj.address_1
                self.fields['address_2'].initial = shipping_address_obj.address_2
                self.fields['city'].initial = shipping_address_obj.city
                self.fields['postcode'].initial = shipping_address_obj.postcode
                self.fields['state'].initial = shipping_address_obj.state
        

    account_type = forms.CharField(max_length=100,required=False)

    firstname = forms.CharField(
        max_length=50,required=True,widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'})
    )
    lastname = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'})
    )
    email = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email'})
    )
    phone = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone'})
    )
    password = forms.CharField(
        max_length=50,required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone'})
    )
    #

    company = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Company'})
    )
    address_1 = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Address 1'})
    )
    address_2 = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Address 2'})
    )
    city = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City'})
    )
    postcode = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Postcode'})
    )
    state = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'State'})
    )
    #

    shipping_address = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Shipping Address'})
    )
 
    cash_on_delivery = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Cash on Delivery'})
    )

    def save(self,cart_data):
        account_type=self.cleaned_data['account_type'],



        firstname=self.cleaned_data['firstname'],
        lastname=self.cleaned_data['lastname'],
        email=self.cleaned_data['email'],
        phone=self.cleaned_data['phone'],
    
        if self.request.user.is_authenticated:
            password = self.cleaned_data['password']
            password=password
        else:
            password  = phone[0]

        company=self.cleaned_data['company'],
        address_1=self.cleaned_data['address_1'],
        address_2=self.cleaned_data['address_2'],
        city=self.cleaned_data['city'],
        postcode=self.cleaned_data['postcode'],
        state=self.cleaned_data['state'],

        shipping_address=self.cleaned_data['shipping_address'],

        # free_shipping=self.cleaned_data['free_shipping'],
        cash_on_delivery=self.cleaned_data['cash_on_delivery'],
        

        user_obj = {
            'first_name' : firstname[0],
            'last_name' : lastname[0],
            'email' : email[0],
            'phone' : phone[0],
            'password':password
        }

        if not self.request.user.is_authenticated:
            custom_user = CustomUser.objects.create(**user_obj)
        else:
            custom_user = CustomUser.objects.get(email =  email[0])

        order_id = generate_order_id()
        shipping_ob = False
        order = False
        
        if custom_user:
            for data in cart_data:
                product = data['product_id'][0]
                print(product)
                print("manoj order")

                free_membership_price = data['free_membership_price']
                platinum_membership_price = data['platinum_membership_price']
                b2b_membership_price = data['b2b_membership_price']

                image = data['image']
                quantity = data['quantity']
                brand = data['brand']
                order_obj = {
                    'order_id':order_id,
                    'product_id':product,
                    'free_membership_price':free_membership_price,
                    'platinum_membership_price':platinum_membership_price,
                    'b2b_membership_price':b2b_membership_price,
                    'image' : image,
                    'quantity' : quantity,
                    'brand' : brand,
                    'user':custom_user,
                }
                print(order_obj)
                order = Order.objects.create(**order_obj)

            if order:
                shipping_obj = {
                    'name':firstname[0],
                    'phone':phone[0],
                    'email': email[0],
                    'user':custom_user,
                    'company_name':company[0],
                    'address_1' : address_1[0],
                    'address_2' : address_2[0],
                    'city' : city[0],
                    'postcode':postcode[0],
                    'state':state[0],
                    'order_id':order_id[0]
                }

                shipping_ob = Shipping.objects.create(**shipping_obj)
                shipping_ob = True
            else:
                print("created order failed to create")

     
        return shipping_ob
    
def generate_order_id():
    import datetime
    # Generate a unique order ID based on the current date and time
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    order_id = timestamp
    return order_id

    
