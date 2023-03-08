from django.urls import re_path,path
from . import views

app_name = 'admin-admin'
urlpatterns = [
    re_path(r'^(?P<username>[\w]+)/$',views.AdminPanelView,name='admin-panel'),

    re_path(r'^add-store/$',views.AddStore,name='add-store'),
    re_path(r'^add-ticket/$',views.AddTicket,name='add-ticket'),

    re_path(r'^customer/(?P<pk>[\w]+)/$',views.UserInfo,name='user-info'),
    re_path(r'^store/(?P<pk>[\w]+)/$',views.StoreInfo,name='store-info'),
    re_path(r'^ticket/(?P<pk>[\w]+)/$',views.TicketInfo,name='ticket-info'),

    re_path(r'^delete-store/(?P<pk>[\w]+)/$',views.DeleteStore,name='delete-store'),
    re_path(r'^delete-user/(?P<pk>[\w]+)/$',views.DeleteUser,name='delete-user'),

]