from django.db import models
from django.contrib.auth.models import User
# from django.dispatch import receiver
from django.db.models.signals import post_save
# from parties.models import PartyTicket
# from .extras import generate_order_id
# Create your models here.

class Customer(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    fname = models.CharField(max_length=200,null=True,verbose_name="First name")
    lname = models.CharField(max_length=200,null=True,verbose_name="Last name")
    email = models.EmailField(max_length=200,null=True,unique=True)
    forget_pass_token = models.CharField(max_length=100,blank=True,null=True)


    def is_member(self):
        return self.user.groups.filter(name='customer').exists()

    def __str__(self):
        return f"{self.user}"



# @receiver(post_save,sender=User)
# def create_profile(sender,instance,created,*args,**kwargs):
#     email = User.objects.filter(email=instance.email)
#     if not email:
#         user_profile,created = Customer.objects.get_or_create(
#             email=instance.email,
#             user=instance,
#             fname=instance.first_name,
#             lname = instance.last_name,
#         )
#         user_profile.save()

#         cart,is_created=user_profile.cart_set.get_or_create(customer=user_profile)
#         if is_created:
#             cart.ref_code = generate_order_id()
#             cart.customer = user_profile
#             cart.save()