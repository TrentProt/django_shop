from django.contrib import messages
from django.contrib.auth import authenticate, get_user_model, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django_email_verification import send_email
from .forms import UserCreateForm, LoginForm, UserUpdateForm

User = get_user_model()

def register_user(request):
    if request.method == 'POST':
        print(request.POST)
        form = UserCreateForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            user = form.save(commit=False)
            user_email = form.cleaned_data.get('email')
            user_username = form.cleaned_data.get('username')
            user_password = form.cleaned_data.get('password1')
            user = User.objects.create_user(username=user_username, email=user_email, password=user_password)
            send_email(user)
            return redirect('account:email_verification')
    else:
        form = UserCreateForm()
    return render(request, 'account/register.html', {'form': form})

def login_user(request):
    if request.user.is_authenticated:
        return redirect('shop:products')

    if request.method == 'POST':
        form = LoginForm(request.POST)
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('shop:products')
        else:
            messages.info(request, 'Неправильный логин или пароль')
            return redirect('account:login')
    else:
        form = LoginForm()
    return render(request, 'account/login.html', {'form': form})

def logout_user(request):
    logout(request)
    return redirect('shop:products')

@login_required(login_url='account:login')
def dashboard_user(request):
    return render(request, 'account/dashboard.html')

@login_required(login_url='account:login')
def profile_user(request):
    user = request.user
    email = user.email
    print(email)
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=user)
        # С помощью этого валидация на форме, передавая instance
        if form.is_valid():
            user.username = form.cleaned_data.get('username')
            user.email = form.cleaned_data.get('email')
            print(user.email)
            password = form.cleaned_data.get('password')
            if password:
                user.set_password(password)
            user.is_active = False
            user.save()
            if email != user.email:
                send_email(user)
                return redirect('account:email_verification')
            return redirect('account:dashboard')
    else:
        form = UserUpdateForm(instance=user)
    return render(request, 'account/profile.html', {'form': form})

@login_required(login_url='account:login')
def delete_user(request):
    user = User.objects.get(id=request.user.id)
    if request.method == 'POST':
        user.delete()
        return redirect('shop:products')
    return render(request, 'account/account_delete.html')
