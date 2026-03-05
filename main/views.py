from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.messages import success
from django.core.paginator import Paginator
from django.views.decorators.cache import never_cache
from .forms import EmailAuthenticationForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect
from main.forms import ClientRegistrationForm
from .models import Product, ProductCategory, Order, OrderItem
from .telegram import send_telegram_message
from django.shortcuts import get_object_or_404
from .cart import Cart
from .forms import ProfileForm, UserEditForm


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

def get_category_catalog(request):
    categories = ProductCategory.objects.all()

    context = {
        'categories': categories,
    }
    return render(request, 'catalog.html', context)

def get_catalog(request, id):

    category = get_object_or_404(ProductCategory, id=id)
    products = Product.objects.filter(category=category)
    # paginator = Paginator(products, 12)
    # page_number = request.GET.get('page')
    # page_obj = paginator.get_page(page_number)

    context = {
        'products': products,
        'category': category,
    }
    return render(request, 'category.html', context)

def get_delivery(request):
    return render(request, 'delivery.html')

def get_contacts(request):
    return render(request, 'contacts.html')

def cart_add(request, product_id):
    if request.method != "POST":
        return JsonResponse({"error": "Только POST"}, status=405)

    product = get_object_or_404(Product, pk=product_id)

    cart = Cart(request)

    quantity = int(request.POST.get('quantity', 1))
    if quantity < 1:
        quantity = 1

    cart.add(product_id=product_id, quantity=quantity)

    # return redirect('cart_detail')

    return JsonResponse({
        "success": True,
        "product_name": product.name,
        "quantity_added": quantity,
        "total_items": sum(item["quantity"] for item in cart.cart.values()),
        "message": f"Добавлено {quantity} × {product.name}"
    })


def cart_detail(request):
    cart_obj = Cart(request)
    products_in_cart = []
    total_price = 0

    # Собираем данные о товарах из базы по ID из корзины
    for p_id, item in cart_obj.cart.items():
        product = Product.objects.get(id=p_id)
        item_total = product.price * item['quantity']
        total_price += item_total
        products_in_cart.append({
            'product': product,
            'quantity': item['quantity'],
            'total_price': item_total
        })

    return render(request, 'basket.html', {
        'cart_items': products_in_cart,
        'total_price': total_price
    })


def checkout(request):
    cart = Cart(request)

    # Если корзина пуста — назад в корзину
    if not cart.cart:
        messages.warning(request, "Ваша корзина пуста")
        return redirect('cart_detail')

    if request.method == 'POST':
        # Собираем данные из формы
        guest_name = request.POST.get('guest_name', '') if not request.user.is_authenticated else ''
        guest_email = request.POST.get('guest_email', '') if not request.user.is_authenticated else ''
        guest_phone = request.POST.get('guest_phone', '') if not request.user.is_authenticated else ''
        delivery_address = request.POST.get('delivery_address', '').strip()
        phone = request.POST.get('phone', request.user.profile.phone if hasattr(request.user, 'profile') else '').strip()
        payment_method = request.POST.get('payment_method')
        comment = request.POST.get('comment', '').strip()

        # Валидация (минимальная)
        errors = []
        if not delivery_address:
            errors.append("Укажите адрес доставки")
        if not phone:
            errors.append("Укажите телефон для связи")
        if not payment_method or payment_method not in dict(Order.PAYMENT_CHOICES):
            errors.append("Выберите корректный способ оплаты")

        if errors:
            for msg in errors:
                messages.error(request, msg)
            # Лучше возвращать render с данными, а не redirect — пользователь не потеряет введённое
            context = {
                'delivery_address': delivery_address,
                'phone': phone,
                'payment_method': payment_method,
                'comment': comment,
                'cart_items': [...],  # как у тебя было
                'total_price': cart.get_total_price(),
                'payment_choices': Order.PAYMENT_CHOICES,
            }
            return render(request, 'checkout.html', context)

        # Создаём заказ
        order = Order.objects.create(
            user=request.user if request.user.is_authenticated else None,
            guest_name=guest_name,
            guest_email=guest_email,
            guest_phone=phone,
            delivery_address=delivery_address,
            phone=phone,
            payment_method=payment_method,
            comment=comment,
            status='new'
        )

        # Переносим товары из корзины в заказ
        total = 0
        for p_id, item in cart.cart.items():
            try:
                product = Product.objects.get(id=p_id)
                price = product.price or 0
                OrderItem.objects.create(
                    order=order,
                    product=product,
                    quantity=item['quantity'],
                    price_at_order=price
                )
                total += price * item['quantity']
            except Product.DoesNotExist:
                # Товар удалили — пропускаем
                continue

        # Сохраняем итоговую сумму
        order.total_price = total
        order.save()

        # Очищаем корзину
        cart.clear()

        messages.success(request, f"Заказ №{order.id} успешно оформлен! Мы свяжемся с вами в ближайшее время.")
        return redirect('profile')  # или на страницу "Спасибо за заказ"

    # GET — показываем форму оформления
    context = {
        'cart_items': [],  # для отображения товаров
        'total_price': 0,
        'user': request.user,
    }

    # Заполняем товары для предпросмотра
    for p_id, item in cart.cart.items():
        try:
            product = Product.objects.get(id=p_id)
            item_total = product.price * item['quantity']
            context['cart_items'].append({
                'product': product,
                'quantity': item['quantity'],
                'total': item_total
            })
            context['total_price'] += item_total
            context['payment_choices'] = Order.PAYMENT_CHOICES
        except Product.DoesNotExist:
            pass

    return render(request, 'checkout.html', context)


def orders(request):
    orders = request.user.orders.all()[:10]  # последние 10 заказов
    context = {
        'orders': orders,
    }
    return render(request, 'orders.html', context)


def order_detail(request, order_id):
    # Получаем заказ, но только если он принадлежит текущему пользователю
    order = get_object_or_404(Order, id=order_id, user=request.user)

    # Получаем все позиции заказа
    items = order.items.select_related('product').all()

    context = {
        'order': order,
        'items': items,
        'total_price': order.total_price,
    }
    return render(request, 'order_detail.html', context)


@never_cache
@csrf_protect
def account_auth(request):

    if request.user.is_authenticated:
        messages.info(request, 'Вы уже вошли в систему')
        return redirect('profile')

    login_form = EmailAuthenticationForm(request)
    reg_form = ClientRegistrationForm()

    if request.method == 'POST':
        if 'login_submit' in request.POST:      # отличаем по имени кнопки
            login_form = EmailAuthenticationForm(request, data=request.POST)
            if login_form.is_valid():
                user = login_form.get_user()
                login(request, user)
                messages.success(request, 'Вы успешно вошли!')
                next_url = request.POST.get('next') or request.GET.get('next') or 'profile'
                return redirect(next_url)
            else:
                messages.error(request, 'Ошибка входа. Проверьте email и пароль.')

        elif 'register_submit' in request.POST:
            reg_form = ClientRegistrationForm(request.POST)
            if reg_form.is_valid():
                user = reg_form.save()
                login(request, user)
                messages.success(request, 'Регистрация прошла успешно! Добро пожаловать!')
                return redirect('profile')
            else:
                messages.error(request, 'Ошибка регистрации. Проверьте введённые данные.')

    context = {
        'login_form': login_form,
        'reg_form': reg_form,
        'next': request.GET.get('next', ''),
    }
    return render(request, 'login.html', context)


@login_required
def profile(request):
    profile = request.user.profile

    orders_count = request.user.orders.count()

    role = profile.role

    if role == 'admin':
        template = ''
    elif role == 'manager':
        template = 'manager.html'
    else:
        template = 'profile_user.html'

    context = {
        'profile': profile,
        'user': request.user,
        'is_admin': role == 'admin',
        'is_manager': role == 'manager',
        'is_client': role == 'client',
        'orders_count': orders_count,

    }
    return render(request, template, context)


@login_required
def profile_edit(request):
    profile = request.user.profile

    if request.method == 'POST':
        user_form = UserEditForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=profile)

        if user_form.is_valid() and profile_form.is_valid():
        # if profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Профиль успешно обновлён')
            return redirect('profile')  # или 'profile_edit' — если хотите остаться на странице
        else:
            messages.error(request, 'Проверьте введённые данные')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileForm(instance=profile)

    context = {
        'profile_form': profile_form,
        'user_form': user_form,   # если используете
        'profile': profile,
    }

    return render(request, 'profile_edit.html', context)