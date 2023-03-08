from django.shortcuts import render,redirect
from .decorators import unauthenticate_user,allowed_users
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import get_user_model
from .models import Customer
from .forms import RegisterForm,UpdateUser
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from admin_panel.models import Cart,CartItem
from parties.models import PartyTicket
from django.shortcuts import get_object_or_404
from account.models import Customer
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage
from .tokens import account_activation_token
from .extras import generate_order_id
import uuid
from django.conf import settings
# Create your views here.

def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        customer,created = Customer.objects.get_or_create(
                email=user.email,
                user=user,
                fname=user.first_name,
                lname = user.last_name,
        )
        if created:
            customer.save()

            cart,is_created=customer.cart_set.get_or_create(customer=customer)
            if is_created:
                cart.ref_code = generate_order_id()
                cart.customer = customer
                cart.save()
            #add user to customer group
            group = Group.objects.get(name = 'customer')
            user.groups.add(group)

        messages.success(request, 'Thank you for your email confirmation. Now you can login your account.')
    else:
        messages.error(request, 'Activation link is invalid!')
    return redirect('account:login')

def activateEmail(request, user, to_email):
    mail_subject = 'Activate your user account.'
    message = render_to_string('template_activate_account.html', {
        'user': user.username,
        'domain': get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
        'protocol': 'https' if request.is_secure() else 'http'
    })
    email = EmailMessage(mail_subject, message, to=[to_email])
    if email.send():
        messages.warning(request, 'Dear {{user}} please go to your E-mail {{user.email}} Inbox and click on received activation link to confirm and complete  the registration( Note : Check Your spam folder )')
    else:
        user.delete()
        messages.error(request, f'Problem sending confirmation email to {to_email}, check if you typed it correctly.')

@unauthenticate_user
def RegisterView(request):
    
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        # Check email and username in db
        # Return None if the user or email exists
        username = User.objects.filter(username=str(request.POST.get('username')).lower())
        email = User.objects.filter(email=request.POST.get('email'))
        if username or email:
            if username:
                messages.error(request,"The username is already in use.")
            if email:
                messages.error(request,"The email is already in use.")
        # If email and username were valid , check the form validity
        elif form.is_valid():
            # creating user
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            email = form.cleaned_data.get('email')
            
            activateEmail(request,user,email)

            messages.success(request,f'Dear {user} please go to your E-mail {email} Inbox and click on received activation link to confirm and complete  the registration( Note : Check Your spam folder )')
            return redirect('account:login')
        
        else:
            messages.error(request,"An error has occured during registering.")

    context = {}
    return render(request,'account/register.html',context)

@unauthenticate_user
def LoginView(request):
    if request.method == "POST":
        username = str(request.POST.get('username')).lower()
        password = request.POST.get('password')
        
        user = authenticate(request,username=username,password=password)
            
        if user is not None:
            login(request,user)
            return redirect("/")
        else:
            messages.error(request,"Username or password is wrong.")
    context = {}
    return render(request,'account/login.html',context)

@login_required(login_url='account:login')
def LogoutView(request):
    logout(request)
    return redirect("/")

@login_required(login_url='account:login')
@allowed_users(['customer'])
def CustomerProfileView(request,username):
    form = UpdateUser(instance=request.user.customer)
    cart_items = CartItem.objects.filter(cart__customer__user__username=username).order_by('-created_date')
    cart = Cart.objects.get(customer__user__username=username)

    customer = get_object_or_404(Customer,user__username=username)
    if request.method == 'POST':
        form = UpdateUser(request.POST,instance=request.user.customer)
        if form.is_valid():
            user = form.save()
            if user:
                messages.success(request,"Profile has been updated successfully")
            else:
                messages.error(request,'Unsuccessful')
            return redirect(request.META.get('HTTP_REFERER'))
    context = {
        'form':form,
        'cart_items':cart_items,
        'customer':customer,
        'cart':cart,
    }
    return render(request,"account/user-profile.html",context)

@login_required(login_url='account:login')
@allowed_users(['customer'])
def AddToCart(request,pk):
    # get the user profile
    user_profile = get_object_or_404(Customer, user=request.user)
    product = get_object_or_404(PartyTicket,id=pk)

    # create cart item of the selected product
    cart_item,status = CartItem.objects.get_or_create(product=product,cart__customer__user__username=user_profile,is_ordered=False)

    # check if the user already owns this product
    if status is False:
        messages.info(request,"You already own this product")

    else:
        cart = Cart.objects.get(customer__user__username = user_profile)
        cart.items.add(cart_item)
        messages.info(request, "Item added to cart")
        
    return redirect(request.META.get('HTTP_REFERER'))

@login_required(login_url='account:login')
@allowed_users(['customer'])
def RemoveFromCart(request,pk):
    item = CartItem.objects.get(id=pk,cart__customer__user__username=request.user.customer)
    item.delete()
    return redirect(request.META.get('HTTP_REFERER'))

@login_required(login_url='account:login')
@allowed_users(['customer'])
def IncreaseQuantity(request,pk):
    item = CartItem.objects.get(id=pk)
    item.update_quantity()
    return redirect(request.META.get('HTTP_REFERER'))

@login_required(login_url='account:login')
@allowed_users(['customer'])
def DecreaseQuantity(request,pk):
    item = CartItem.objects.get(id=pk)
    item.decrease_quantity()
    return redirect(request.META.get('HTTP_REFERER'))

def ForgotPassword(request):
    if request.method == 'POST':
        username = request.POST.get('username')

        if not User.objects.filter(username=username).first():
            messages.warning(request,"Username doesn't exist.")

        else:
            email = get_object_or_404(User,username=username).email
            token = str(uuid.uuid4())

            customer = get_object_or_404(Customer,user__username=username)
            customer.forget_pass_token=token
            customer.save()

            subject = "Forgotten Password Link"
            message = f"Click on the link to change your password {request.scheme}://{request.META['HTTP_HOST']}/account/change-password/{token}/"
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [email]
            l = EmailMessage(subject,message,email_from,recipient_list)
            if l.send():
                messages.warning(request, 'An email has been sent to your username email')
            else:
                messages.error(request, 'Email doesn\'t send successfully')

        return redirect('.')
    return render(request,'account/forgot_pass_username.html',context={})

def ChangePassword(request,token):
    profile_obj = get_object_or_404(Customer,forget_pass_token=token)

    if request.method == 'POST':
        new_password = request.POST.get('new_password')
        # confirm_password = request.POST.get('confirm_password')
        user_id = request.POST.get('user_id')

        if not user_id:
            messages.error(request,'No user id found')
            return redirect('.')
        
        else:
            user_obj = get_object_or_404(User,id=user_id)
            user_obj.set_password(new_password)
            user_obj.save()
            messages.success(request,'Password has been changed.')
            return redirect('account:login')
    return render(request,'account/forgot_pass.html',context={'user_id':profile_obj.user.id})