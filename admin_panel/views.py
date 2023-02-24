from django.shortcuts import render,redirect
from .forms import AddStoreForm,AddTicketForm
from django.contrib.auth.models import User,Group
from .models import CartItem
from account.models import Customer
from django.contrib import messages
from account.decorators import allowed_users
from django.contrib.auth.decorators import login_required
from parties.models import PartyTicket,Store
from django.shortcuts import get_object_or_404
# Create your views here.
@login_required(login_url="/account/login/")
@allowed_users(['admin'])
def AddStore(request):
    form = AddStoreForm()
    if request.method == 'POST':
        form = AddStoreForm(request.POST)
        email = User.objects.filter(email=request.POST.get('email'))
        if email:
            messages.error(request,"The email is already in use.")
        elif form.is_valid():
            
            #create store model
            user = form.save()

            store,created = Store.objects.get_or_create(
                email=form.cleaned_data.get('email'),
                username=user,
                name=form.cleaned_data.get('store_name'),
                address = form.cleaned_data.get('venue'),
            )
            store.save()
            # add user to store group
            group = Group.objects.get(name='store')
            user.groups.add(group)

            messages.success(request,"Store was created successfully.")
        else:
            messages.error(request,form.errors)
        
    return render(request,'admin/add_store.html',context={'form':form})

@login_required(login_url="/account/login/")
@allowed_users(['admin'])
def AdminPanelView(request,username):
    customers= Customer.objects.all()
    tickets = PartyTicket.objects.all().order_by('-start_date')
    expired_tickets = tickets.exclude(status='selling')
    stores = Store.objects.all()
    purchased_tickets = CartItem.objects.filter(is_ordered=True).order_by('-created_date')
    context={
        "customers":customers,
        "tickets":tickets,
        'purchased_tickets':purchased_tickets,
        'stores':stores,
        'expired_tickets':expired_tickets
    }
    return render(request,'admin/admin-panel.html',context)

@login_required(login_url="/account/login/")
@allowed_users(['admin'])
def UserInfo(request,pk):
    customer = get_object_or_404(Customer,id=pk)
    products = customer.cart_set.all()[0].items.filter(is_ordered=True).order_by('-created_date')
    context={
        'customer':customer,
        'products':products,
    }
    return render(request,'admin/user-info.html',context)

@login_required(login_url="/account/login/")
@allowed_users(['admin'])
def StoreInfo(request,pk):
    store = get_object_or_404(Store,id=pk)
    tickets = PartyTicket.objects.filter(provider__username__username=store)
    context = {
        'store':store,
        'tickets':tickets
    }
    return render(request,'admin/store-info.html',context)

@login_required(login_url="/account/login/")
@allowed_users(['admin'])
def DeleteStore(request,pk):
    store = get_object_or_404(Store,id=pk)
    user = get_object_or_404(User,username=store)
    user.delete()
    return redirect(f'/panel/{request.user}/')

@login_required(login_url="/account/login/")
@allowed_users(['admin'])
def DeleteUser(request,pk):
    customer = get_object_or_404(Customer,id=pk)
    user = get_object_or_404(User,username=customer)
    cart_items = CartItem.objects.filter(product__provider__username__username=user)
    user.delete()
    cart_items.delete()
    return redirect(f'/panel/{request.user}/')

@login_required(login_url="/account/login/")
@allowed_users(['admin'])
def AddTicket(request):
    if request.method == 'POST':
        provider_id = get_object_or_404(Store,username__username=request.POST['provider'])
        lst = [request.POST['start-date'],request.POST['start-hour']]
        ticket,created = PartyTicket.objects.get_or_create(
            name =  request.POST['name'],
            provider = provider_id,
            price = request.POST['price'],
            start_date = ' '.join(lst),
            description = request.POST['description'],
            status= "selling"
        )
        if created:
            ticket.save()
            messages.info(request,'Ticket has been added successfully.')
        else:
            messages.info(request,"Ticket has been already added.")
    context={}
    return render(request,'admin/add_ticket.html',context)