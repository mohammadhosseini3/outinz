from django.urls import re_path
from . import views

app_name = "payment"

urlpatterns = [
    re_path(r'^create_product/$',views.CreateProduct,name='create_product'),
    re_path(r'^webhook/',views.stripe_webhook,name='webhook'),    
    re_path(r'^success/',views.success_page,name='success'), 
    re_path(r'^cancel/',views.cancel_page,name='cancel'), 
]