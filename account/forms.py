from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Customer
from parties.models import Store

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','first_name','last_name','email','password1','password2']

class UpdateUser(ModelForm):
    class Meta:
        model = Customer
        fields = ['fname','lname']

class EditProviderForm(ModelForm):
    class Meta:
        model = Store
        fields = ['name','address']
