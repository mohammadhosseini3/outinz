from django.conf import settings
from admin_panel.models import Cart
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.core.mail import send_mail
import stripe
from django.utils import timezone


# Create your views here.
stripe.api_key = settings.STRIPE_SECRET_KEY
def CreateProduct(request):
    cart = Cart.objects.get(customer__user_id=request.user.id)
    total_price = cart.total_price*100
    try:
        checkout = stripe.checkout.Session.create(
            payment_method_types = ["card"],
            line_items=[
                    {
                        'price_data': {
                            'currency': 'try',
                            'unit_amount': total_price,
                            'product_data': {
                                'name': 'Party Ticket',
                            },
                        },
                        'quantity': 1,
                    },
                ],
                metadata={
                    "product_id": cart.id
                },
            customer_email = cart.customer.email,
            mode = "payment",
            success_url = f"http://127.0.0.1:8000/payment/success/",
            cancel_url = f"http://127.0.0.1:8000/payment/cancel/",
        )
        return redirect(checkout.url,code = 303)

    except Exception as e:
        return e

@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
        
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    if event['data']['object']['metadata']:
        cart_id = event['data']['object']['metadata']['product_id']

    # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        customer_email = event['data']['object']['customer_details']['email']
        customer = event['data']['object']['customer_details']['name']
        cart = Cart.objects.get(id=cart_id)
        items = cart.items.filter(is_ordered=False)
        items.update(is_ordered=True,created_date=timezone.now())
        subject = 'Payment was successful'
        message = f'Dear {customer}, thanks for your purchase.\nTickets: {",".join([item.product.name for item in items])}\nYour tickets code is {cart.ref_code}.\nKeep your code in secret.\nThanks'
        email_from = settings.EMAIL_HOST_USER
        send_mail(subject,message,email_from,(customer_email,))
    # elif event["type"] == "payment_intent.succeeded":
    #     print("payment_intent.succeeded")
    return HttpResponse(status=200)


def success_page(request):
    context={}
    return render(request,"payment/success.html",context)

def cancel_page(request):
    context={}
    return render(request,"payment/success.html",context)