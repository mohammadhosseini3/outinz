from django.contrib.auth.forms import UserCreationForm
from account.models import Customer
from django import forms
from parties.models import PartyTicket
from django.contrib.auth.models import User

class AddStoreForm(UserCreationForm):
    venue = forms.CharField(max_length=100,required=False)
    store_name = forms.CharField(max_length=100)
    class Meta:
        model = User
        fields = ['username','password1','password2','store_name','venue','email']

class EditUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name','last_name','email']

# class EditCustomerForm(forms.ModelForm):
#     class Meta:
#         model = Customer
#         fields = ['fname','lname','email']

class EditTicketForm(forms.ModelForm):
    class Meta:
        model = PartyTicket
        fields = '__all__'