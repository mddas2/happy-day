from django import template
import json

register = template.Library()

@register.simple_tag
def break_loop():
   raise StopIteration("Loop was stopped by custom tag")

@register.simple_tag
def getCartData(request):
    cart_data_str = request.COOKIES.get('cart')
    cart_data = json.loads(cart_data_str) if cart_data_str else []
    return cart_data

@register.simple_tag
def calculate_cart_price(request):
   cart_data_str = request.COOKIES.get('cart')
   cart_data = json.loads(cart_data_str) if cart_data_str else []

   total_free_membership_price = 0
   total_platinum_membership_price = 0
   total_b2b_membership_price = 0

   for data in cart_data:
      quantity = data['quantity']

      free_membership_price = data['free_membership_price']
      total_free_membership_price = int(quantity)*(int(free_membership_price)+total_free_membership_price)

      platinum_membership_price = data['platinum_membership_price']
      total_platinum_membership_price = int(quantity)*(int(platinum_membership_price)+total_platinum_membership_price)

      
      b2b_membership_price = data['b2b_membership_price']
      total_b2b_membership_price = int(quantity)*(int(b2b_membership_price)+total_b2b_membership_price)
   
   data = {
      'total_b2b_membership_price':total_b2b_membership_price,
      'total_platinum_membership_price':total_platinum_membership_price,
      'total_free_membership_price':total_free_membership_price
   }

   # print(data)

   return data


@register.simple_tag
def is_greater_cart(request):
   cart_data_str = request.COOKIES.get('cart')
   cart_data = json.loads(cart_data_str) if cart_data_str else []

   if(len(cart_data)>0):
      return True
   else:
      return False

