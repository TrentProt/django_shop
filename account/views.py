from django.contrib import messages
from django.contrib.auth import authenticate, get_user_model, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django_email_verification import send_email
from .forms import UserCreateForm

User = get_user_model()

def register_user(request):
    if request.method == 'POST':
        print(request.POST)
        form = UserCreateForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            user = form.save(commit=False)
            user.is_active = False
            user_email = form.cleaned_data.get('email')
            user_username = form.cleaned_data.get('username')
            user_password = form.cleaned_data.get('password1')

            user = User.objects.create_user(username=user_username, email=user_email, password=user_password)

            send_email(user)
            print(2)
            return redirect('/account/email_verification/')
    else:
        form = UserCreateForm()
    return render(request, 'account/register.html', {'form': form})