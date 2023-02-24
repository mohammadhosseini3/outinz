from django.shortcuts import render,redirect
from account.models import Customer
from parties.models import PartyTicket
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
# Create your views here.
def HomePage(request):
    if request.method=='POST':
        check = send_mail(
            f"{request.POST.get('sender_email')}",
            f"{request.POST.get('sender_name')}\n{request.POST.get('message')}",
            request.POST.get('sender_email'),
            settings.ADMIN_EMAILS
        )
        if check:
            messages.info(request,'Email has been sent successfully.')
        else:
            messages.error(request,'Email has not been sent successfully.')
        return redirect('home:home')
    group = request.user.groups.all()
    customers_number = Customer.objects.all().count()
    party_ticket_number = PartyTicket.objects.filter(status='selling').count()
    if group.exists():
        group = request.user.groups.all()[0]
    context = {
        'group':str(group),
        'customers_number':customers_number,
        'party_ticket_number':party_ticket_number,
    }
    return render(request,"home/index.html",context)