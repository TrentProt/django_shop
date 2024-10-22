from django.urls import path
from .views import payment_success, payment_fail, shipping, checkout, complete_order

app_name = 'payment'

urlpatterns = [
    path('payment_success/', payment_success ,name='payment_success'),
    path('payment_fail/', payment_fail ,name='payment_fail'),
    path('shipping/', shipping, name='shipping'),
    path('checkout/', checkout, name='checkout'),
    path('complete_order/', complete_order, name='complete_order'),
]