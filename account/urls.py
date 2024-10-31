from django.urls import path, reverse_lazy
from .views import register_user, login_user, logout_user, dashboard_user, profile_user, delete_user
from django.shortcuts import render
from django.contrib.auth import views as auth_views

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
    path('delete_account/', delete_user, name='delete'),

    path('password_reset/', auth_views.PasswordResetView.as_view(
        template_name='account/password_reset/password_reset.html',
        email_template_name='account/password_reset/password_reset_email.html',
        success_url=reverse_lazy('account:password_reset_done')
    ),
        name='password_reset'),

    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='account/password_reset/password_reset_done.html'
    ),
         name='password_reset_done'),

    path('password_reset_confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='account/password_reset/password_reset_confirm.html',
        success_url=reverse_lazy('account:password_reset_complete')
    ),
         name='password_reset_confirm'),

    path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name='account/password_reset/password_reset_complete.html'
    ),
         name='password_reset_complete'),


]
