from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
# Create your models here.

class PartyVenue(models.Model):
    venue = models.CharField(max_length=50,verbose_name="Venue",null=True)
    location = models.CharField(max_length=50,verbose_name="Location",null=True)
    def __str__(self):
        return f"{self.location}-{self.venue}"
    
class Store(models.Model):
    username = models.OneToOneField(User,on_delete=models.CASCADE,null=True)
    name = models.CharField(max_length=100,verbose_name="Name",null=True)
    address = models.CharField(max_length=200,verbose_name="Address",null=True)
    email = models.CharField(max_length=100,verbose_name="Email",null=True)
    class Meta:
        verbose_name="Provider"
    def __str__(self):
        return self.username.username
    
class PartyTicket(models.Model):
    name =  models.CharField(max_length=50,verbose_name="Party Name",null=True)
    provider = models.ForeignKey(Store,on_delete=models.CASCADE,null=True)
    price = models.IntegerField(null=True)
    start_date = models.DateTimeField(verbose_name="Start Date",null=True)
    description = models.TextField(null=True,blank=True)
    TICKET_STATUS = [
        ('cancled','Cancled'),
        ('expired','Expired'),
        ('sold out','Sold out'),
        ('selling','Selling'),
    ]
    status = models.CharField(max_length=10,choices=TICKET_STATUS,default='Selling')
    
    def is_expired(self):
        if self.start_date <= timezone.now():
            self.status = 'expired'
            self.save()
            return True

    def __str__(self):
        return f"{self.name}-{self.provider.name}-{self.price}-{self.status}"
