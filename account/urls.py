from django.urls import path
from .views import register_user, login_user, logout_user, dashboard_user, profile_user, delete_user
from django.shortcuts import render

app_name = 'account'

urlpatterns = [
    path('register/', register_user, name='registration'),
    path('email_verification/',
         lambda request:render(request, 'account/email/email_verification.html'),
         name='email_verification'),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
    path('dashboard/', dashboard_user, name='dashboard'),
    path('profile/', profile_user, name='profile'),
    path('delete_account', delete_user, name='delete'),
]

# ljph erkq ieet ticc