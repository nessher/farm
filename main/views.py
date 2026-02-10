from django.contrib import messages
from django.contrib.messages import success
from django.views.decorators.cache import never_cache
from .forms import EmailAuthenticationForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect
from main.forms import ClientRegistrationForm
from .telegram import send_telegram_message


def get_main(request):
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        email = request.POST.get('email', '').strip()
        phone = request.POST.get('phone', '').strip()
        message = request.POST.get('message', '').strip()

        if not name or not phone:
            return render(request, 'home_page.html',{
                'error': 'Имя и телефон обязательны',
                'name': name,
                'last_name': last_name,
                'email': email,
                'phone': phone,
                'message': message,
            })

        print("!!! Данные получены, готовим сообщение !!!")
        print(f"Имя: {name}, Телефон: {phone}")

        telegram_text = (
            '<b>Новая заявка с сайта!</b>\n\n'
            f"👤 Клиент: <b>{name} {last_name}</b>\n"
            f"📞 Телефон: <b>{phone}</b>\n"
        )
        if email:
            telegram_text += f'✉️ Email: {email}\n'
        if message:
            telegram_text += f'\n💬 Сообщение:\n{message}'

        print("!!! Пытаемся отправить в Telegram !!!")
        print("Текст сообщения:")
        print(telegram_text)

        success = send_telegram_message(telegram_text)

        print(f"!!! Результат отправки: {success} !!!")

        if success:
            print('успех')
            messages.success(request, 'Спасибо! Заявка отправлена. Мы свяжемся с вами в ближайшее время.')
            return redirect(request.path)
        else:
            return render(request, 'home_page.html', {
                'error': 'Ошибка отправки. Попробуйте еще раз.',
                'name': name,
                'last_name': last_name,
                'email': email,
                'phone': phone,
                'message': message,
            })
    return render(request, 'home_page.html')

def get_about(request):
    return render(request, 'about_farm.html')

def get_catalog(request):
    return render(request, '')

def get_delivery(request):
    return render(request, 'delivery.html')

def get_contacts(request):
    return render(request, 'contacts.html')

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