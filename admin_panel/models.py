from django.db import models
from account.models import Customer
from parties.models import PartyTicket
from django.contrib.auth.models import AbstractUser


# Create your models here.

class ProductType(models.Model):
    type = models.CharField(max_length=100,verbose_name="Type",null=True)
    def __str__(self):
        return f"{self.type}"

class CartItem(models.Model):
    product = models.ForeignKey(PartyTicket,on_delete=models.CASCADE,null=True)
    is_ordered = models.BooleanField(default=False)
    created_date = models.DateTimeField(null=True)
    quantity = models.IntegerField(default=1)

    class Meta:
        ordering = ('created_date',)

    def total_price(self):
        return self.quantity * self.product.price
    total_price = property(total_price)

    def update_quantity(self):
        self.quantity+=1
        self.save()
    
    def decrease_quantity(self,):
        self.quantity-=1
        self.save()

    def __str__(self):
        return f"{self.quantity} units of {self.product.name} {self.total_price}"

class Cart(models.Model):
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE,verbose_name='Csutomer name',null=True)
    ref_code = models.CharField(max_length=15,blank=True,null=True)
    creation_date = models.DateTimeField(auto_now_add=True,verbose_name='creation date')
    items = models.ManyToManyField(CartItem,blank=True)

    class Meta:
        ordering = ('-creation_date',)

    def get_cart_items(self):
        return self.items.all()
    
    def is_cart_empty(self):
        return self.items.all().count() == 0

    def is_empty(self):
        return self.items.filter(is_ordered=False).count() == 0

    def total_price(self):
        return sum([item.product.price*item.quantity for item in self.items.all() if item.is_ordered is False])
    total_price = property(total_price)

    def total_quantity(self):
        return sum([i.quantity for i in self.items.all()])
    # total_quantity = property(total_quantity)

    def __str__(self):
        return f"{self.customer} - {self.ref_code} - {self.total_price}"