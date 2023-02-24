from django.urls import path,re_path
from home import views
app_name = 'home'
urlpatterns = [
    re_path(r'$',views.HomePage,name='home'),
    
]
