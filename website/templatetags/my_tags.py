from django import template

register = template.Library()

@register.simple_tag
def break_loop():
   raise StopIteration("Loop was stopped by custom tag")

@register.simple_tag
def calculate_cart_price(cart_data):
   total_price = 0
   for data in cart_data:
      quantity = data['quantity']
      price = data['free_membership_price']
      total_price = int(quantity)*(price+total_price)
   return total_price
