from django.shortcuts import render
from django.shortcuts import get_object_or_404
from parties.models import PartyTicket,Store
from admin_panel.models import CartItem
from account.forms import EditProviderForm
from django.contrib import messages

# Create your views here.

def PartyTicketList(request):
    party_ticket = PartyTicket.objects.filter(status='selling')
    return render(request,'home/products.html',context={'party_ticket_list':party_ticket})

def PartyTicketDetail(request,pk):
    ticket = get_object_or_404(PartyTicket,id=pk)
    if request.user.groups.all():
        group = request.user.groups.all()[0]
    else:
        group = None
    context={
        'ticket':ticket,
        'group':str(group)
    }
    return render(request,'home/product-detail.html',context)

def ProviderPanel(request,username):
    form = EditProviderForm(instance=request.user.store)
    if request.method == 'POST':
        form = EditProviderForm(request.POST,instance=request.user.store)
        if form.is_valid():
            user = form.save()
            if user:
                messages.success(request,'Profile has been updated.')
        else:
            messages.error(request,form.errors)
    provider = get_object_or_404(Store,username__username=username)
    provider_tickets = provider.partyticket_set.all().order_by('-start_date')
    purchased_tickets = CartItem.objects.filter(product__provider__username__username=username,is_ordered=True).order_by('-created_date')
    context={
        'form':form,
        'provider':provider,
        'provider_tickets':provider_tickets,
        'purchased_tickets':purchased_tickets
    }
    return render(request,'admin/provider-panel.html',context)