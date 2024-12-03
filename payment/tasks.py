from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail

from .models import Order, ShippingAddress

@shared_task
def send_order_confirmation(order_id):
    order = Order.objects.get(id=order_id)
    subject = f'Order confirmation for order {order.id}'
    receipent_data = ShippingAddress.objects.get(user=order.user)
    receipent_email = receipent_data.email
    message = f'Dear {order.user.username}, \n\n Your order has been successfully placed.'

    mail_to_sender = send_mail(subject, message=message, from_email=settings.EMAIL_HOST_USER,
                               recipient_list=[receipent_email])
    return mail_to_sender

@shared_task
def test(number):
    return int(number)+3