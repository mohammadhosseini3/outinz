from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from django import forms
from parties.models import PartyTicket
from django.contrib.auth.models import User

class AddStoreForm(UserCreationForm):
    venue = forms.CharField(max_length=100,required=False)
    store_name = forms.CharField(max_length=100)
    class Meta:
        model = User
        fields = ['username','password1','password2','store_name','venue','email']

class AddTicketForm(ModelForm):
    class Meta:
        model = PartyTicket
        fields = '__all__'
        exclude = ['status']