from django.urls import re_path
from . import views

app_name = 'party'
urlpatterns = [
    re_path(r'^party-ticket-list/$',views.PartyTicketList,name='party-ticket-list'),
    re_path(r'^party-ticket/(?P<pk>[\w]+)/$',views.PartyTicketDetail,name='party-ticket-detail'),
    re_path(r'^provider/(?P<username>[\w]+)/$',views.ProviderPanel,name='provider-panel'),
]