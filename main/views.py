from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import ensure_csrf_cookie


def get_main(request):
    return render(request, 'main.html')

def get_about(request):
    return render(request, '')

def get_catalog(request):
    return render(request, '')

def get_delivery(request):
    return render(request, '')

def get_contacts(request):
    return render(request, '')

def get_basket(request):
    return render(request, '')

@ensure_csrf_cookie
def get_account_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('main')
        else:
            if User.objects.filter(username=username).exists():
                return JsonResponse({'error': 'invalid_password'})
            else:
                return JsonResponse({'error': 'user_not_exists'})
    return render(request, 'login.html')

@ensure_csrf_cookie
def get_account_register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        if User.objects.filter(username=username).exists():
            return JsonResponse({'error': 'user_exists'})
        user = User.objects.create_user(username=username, email=email, password=password)
        login(request, user)
        return redirect('main')
    return render(request, 'login.html')