from django.urls import re_path,path
from . import views

app_name = 'account'

urlpatterns = [
    re_path(r'^register/$',views.RegisterView,name = 'register'),
    re_path(r'^login/$',views.LoginView,name = 'login'),
    re_path(r'^logout/$',views.LogoutView,name = 'logout'),

    re_path(r'^profile/(?P<username>[\w.@+-]+)/$',views.CustomerProfileView,name = 'user-profile'),

    re_path(r'^add-to-cart/(?P<pk>[\w]+)/$',views.AddToCart,name = 'add-to-cart'),
    re_path(r'^remove-from-cart/(?P<pk>[\w]+)/$',views.RemoveFromCart,name = 'remove-from-cart'),

    re_path(r'^forgot-password-username/$',views.ForgotPassword,name = 'forgot-pass-username'),
    path('change-password/<token>/',views.ChangePassword,name = 'change-password'),

    re_path(r'^increase-quantity/(?P<pk>[\w]+)/$',views.IncreaseQuantity,name = 'increase-quantity'),
    re_path(r'^decrease-quantity/(?P<pk>[\w]+)/$',views.DecreaseQuantity,name = 'decrease-quantity'),
    
    path('activate-user/<uidb64>/<token>',views.activate, name='activate'),
]