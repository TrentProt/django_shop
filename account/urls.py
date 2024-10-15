from django.urls import path
from .views import register_user
from django.shortcuts import render

app_name = 'account'

urlpatterns = [
    path('register/', register_user, name='register'),
    path('email_verification/',
         lambda request:render(request, 'account/email/email_verification.html'),
         name='email_verification')
]

# ljph erkq ieet ticc