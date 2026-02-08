from pyexpat.errors import messages
from django.views.decorators.cache import never_cache
from .forms import EmailAuthenticationForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect
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

@never_cache
@csrf_protect
def account_auth(request):

    login_form = EmailAuthenticationForm(request)   # или твоя EmailAuthenticationForm
    reg_form = ClientRegistrationForm()

    if request.method == 'POST':
        if 'login_submit' in request.POST:      # отличаем по имени кнопки
            login_form = EmailAuthenticationForm(request, data=request.POST)
            if login_form.is_valid():
                user = login_form.get_user()
                login(request, user)
                return redirect('/auth/?just_logged_in=1')

        elif 'register_submit' in request.POST:
            reg_form = ClientRegistrationForm(request.POST)
            if reg_form.is_valid():
                user = reg_form.save()
                login(request, user)
                return redirect('main')

    # GET или невалидный POST → просто показываем страницу
    context = {
        'login_form': login_form,
        'reg_form': reg_form,
    }
    return render(request, 'login.html', context)