from django import forms
from account.models import CustomUser

class CheckOutForm(forms.Form):
    account_type = forms.CharField(max_length=100)

    firstname = forms.CharField(
        max_length=50,required=False,widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'})
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
    free_shipping = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Free Shipping'})
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

        company=self.cleaned_data['company'],
        address_1=self.cleaned_data['address_1'],
        address_2=self.cleaned_data['address_2'],
        city=self.cleaned_data['city'],
        postcode=self.cleaned_data['postcode'],
        state=self.cleaned_data['state'],

        shipping_address=self.cleaned_data['shipping_address'],

        free_shipping=self.cleaned_data['free_shipping'],
        cash_on_delivery=self.cleaned_data['cash_on_delivery'],

        user_obj = {
            'first_name' : firstname,
            'last_name' : lastname,
            'email' : email,
            'phone' : phone,
        }
        custom_user = CustomUser.objects.create(**user_obj)

        shipping_obj = {
            'name':firstname+" "+ lastname,
            'phone':phone,
            'email': email,
            'user_id'
            'company_name':company,
            'address_1' : address_1,
            'address_2' : address_2,
            'city' : city,
            'postcode':postcode,
            'state':state,
            'shipping_address':shipping_address
        }
        cart_data = cart_data
        # order_obj = 
        return True

    
