from pyexpat.errors import messages

from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import ensure_csrf_cookie

from main.forms import ClientRegistrationForm


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

def get_account_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('main')
    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'login_form': form, 'reg_form': ClientRegistrationForm()})

def get_account_register(request):
    print(f"Request method: {request.method}")
    if request.method == 'POST':
        print("POST data:", request.POST)
        form = ClientRegistrationForm(request.POST)
        print("Form bound:", form.is_bound)
        if form.is_valid():
            print("Form is valid! Saving user...")
            user = form.save()
            print(f"User created: {user.pk} - {user.email} / username={user.username}")
            login(request, user)
            return redirect('main')
        else:
            print("Form NOT valid!")
            print("Errors:", form.errors.as_json(indent=2))
            print("Ошибки валидации формы:", form.errors.as_data())
    else:
        form = ClientRegistrationForm()
    return render(request, 'login.html', {'reg_form': form, 'login_form': AuthenticationForm()})