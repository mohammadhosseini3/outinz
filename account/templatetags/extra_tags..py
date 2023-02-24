from django import template
from admin_panel.models import CartItem
register = template.Library()

@register.filter
def increasing_quantity(quantity):
    quantity = quantity-1
    return quantity