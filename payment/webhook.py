from django.http import HttpResponse
from yookassa import Webhook
from .tasks import send_order_confirmation

def yookassa_webhook(request):
    webhook = Webhook(request.body, request.headers['Content-Type'])
    event = webhook.event()
    send_order_confirmation.delay('1')
    if event.type == 'payment.success':
        return HttpResponse(status=200)
    return HttpResponse(status=200)