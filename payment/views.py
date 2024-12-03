import uuid
from imghdr import tests
from locale import currency
from re import match
import uuid
from .tasks import test

from django.conf import settings
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from yookassa import Configuration, Payment
from basket.basket import Basket
from .forms import ShippingAddressForm
from .models import Order, OrderItem, ShippingAddress

Configuration.account_id = settings.YOOKASSA_SHOP_ID
Configuration.secret_key = settings.YOOKASSA_SECRET_KEY

@login_required(login_url='account:login')
def shipping(request):
    test.delay('2')
    try:
        shipping_address = ShippingAddress.objects.get(user=request.user)
    except ShippingAddress.DoesNotExist:
        shipping_address = None
    form = ShippingAddressForm(instance=shipping_address)
    if request.method == 'POST':
        form = ShippingAddressForm(request.POST, instance=shipping_address)
        if form.is_valid():
            shipping_address = form.save(commit=False)
            shipping_address.user = request.user
            shipping_address.save()
            return redirect('account:dashboard')
    return render(request, 'payment/shipping.html', {'form': form})


def payment_success(request):
    for key in list(request.session.keys()):
        del request.session[key]
    return render(request, 'payment/payment_success.html')

def payment_fail(request):
    return render(request, 'payment/payment_fail.html')

def complete_order(request):
    test.delay('2')
    print(request.POST.get)
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        street_address = request.POST.get('street_address')
        apartment_address = request.POST.get('apartment_address')
        city = request.POST.get('city')
        country = request.POST.get('country')
        zip_code = request.POST.get('zip_code')
        basket = Basket(request)
        total_price = basket.get_total_price()


        idemotence_key = uuid.uuid4()
        currency = 'RUB'
        description = 'Товары в корзине'
        payment = Payment.create({
            'amount': {
                'value': str(total_price*100),
                'currency': currency
            },
            'confirmation': {
                'type': 'redirect',
                'return_url': request.build_absolute_uri(reverse('payment:payment_success')),
            },
            'capture': True,
            'test': True,
            'description': description
        }, idemotence_key)

        shipping_address, _ = ShippingAddress.objects.get_or_create(
            user=request.user,
            defaults={
                'full_name': name,
                'email': email,
                'street_address': street_address,
                'apartment_address': apartment_address,
                'country': country,
                'city': city,
                'zip_code': zip_code
            }
        )
        cofirmation_url = payment.confirmation.confirmation_url
        if request.user.is_authenticated:
            order = Order.objects.create(user=request.user, shipping_address=shipping_address, amount=total_price)
            for item in basket:
                OrderItem.objects.create(
                            order=order,
                            product=item['product'],
                            price=item['price'],
                            quantity=item['qty'],
                            user=request.user
                        )
            return redirect(cofirmation_url)
        else:
            order = Order.objects.create(shipping_address=shipping_address,
                                         amount=total_price)
            for item in basket:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    price=item['price'],
                    quantity=item['qty']
                )
        # order = Order.objects.create(user=request.user, shipping_address=shipping_address, amount=total_price)
        # if request.user.is_authenticated:
        #     for item in basket:
        #         OrderItem.objects.create(
        #             order=order,
        #             product=item['product'],
        #             price=item['price'],
        #             quantity=item['qty'],
        #             user=request.user
        #         )
        # else:
        #     for item in basket:
        #         OrderItem.objects.create(
        #             order=order,
        #             product=item['product'],
        #             quantity=item['qty']
        #         )
        # return JsonResponse({'success': True})

def checkout(request):
    if request.user.is_authenticated:
        shipping_address = get_object_or_404(ShippingAddress, user=request.user)
        if shipping_address:
            return render(request, 'payment/checkout.html', {'shipping_address': shipping_address})
    return render(request, 'payment/checkout.html')
