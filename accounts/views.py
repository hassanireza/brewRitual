from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from .models import UserProfile
from loyalty.utils import get_or_create_profile


def register(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password1 = request.POST.get('password1', '')
        password2 = request.POST.get('password2', '')
        first_name = request.POST.get('first_name', '').strip()

        errors = []
        if not username:
            errors.append('Username is required.')
        elif User.objects.filter(username=username).exists():
            errors.append('That username is already taken.')
        if not email:
            errors.append('Email is required.')
        if len(password1) < 8:
            errors.append('Password must be at least 8 characters.')
        if password1 != password2:
            errors.append('Passwords do not match.')

        if errors:
            for e in errors:
                messages.error(request, e)
            return render(request, 'accounts/register.html', {'username': username, 'email': email, 'first_name': first_name})

        user = User.objects.create_user(username=username, email=email, password=password1, first_name=first_name)
        UserProfile.objects.get_or_create(user=user)
        get_or_create_profile(user)
        login(request, user)
        messages.success(request, f'Welcome to Brew Ritual, {first_name or username}. Your ritual begins now.')
        return redirect('home')

    return render(request, 'accounts/register.html')


def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            get_or_create_profile(user)
            next_url = request.GET.get('next', 'home')
            return redirect(next_url)
        messages.error(request, 'Invalid credentials. Please try again.')
    return render(request, 'accounts/login.html')


def logout_view(request):
    logout(request)
    messages.info(request, 'You have been signed out. See you next time.')
    return redirect('home')


@login_required
def profile(request):
    user_profile, _ = UserProfile.objects.get_or_create(user=request.user)
    loyalty_profile = get_or_create_profile(request.user)

    if request.method == 'POST':
        request.user.first_name = request.POST.get('first_name', '').strip()
        request.user.last_name = request.POST.get('last_name', '').strip()
        request.user.email = request.POST.get('email', '').strip()
        request.user.save()
        user_profile.phone = request.POST.get('phone', '').strip()
        user_profile.bio = request.POST.get('bio', '').strip()
        user_profile.save()
        messages.success(request, 'Profile updated.')
        return redirect('accounts:profile')

    return render(request, 'accounts/profile.html', {
        'user_profile': user_profile,
        'loyalty_profile': loyalty_profile,
    })
