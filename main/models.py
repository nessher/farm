# from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from django.db import models
from django.utils import timezone

class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='profile',
    )
    ROLE_CHOICES = [
        ('client', 'Клиент'),
        ('manager', 'Менеджер'),
        ('admin', 'Администратор'),
    ]
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='client',
        verbose_name='Роль'
    )
    phone = models.CharField(max_length=20, blank=True, verbose_name='Телефон')

    first_name = models.CharField(max_length=100, blank=True, verbose_name='Имя')
    last_name = models.CharField(max_length=100, blank=True, verbose_name='Фамилия')
    middle_name = models.CharField(max_length=100, blank=True, verbose_name='Отчество')

    lifetime_spent = models.DecimalField(
        max_digits=12, decimal_places=2, default=0, verbose_name='Общая сумма покупок'
    )

    def __str__(self):
        return f"Профиль {self.user.email or self.user.username}"

    def get_full_name(self):
        parts = [self.first_name, self.last_name]
        return " ".join(filter(None, parts)) or "Клиент"

    class Meta:
        verbose_name = "профиль пользователя"
        verbose_name_plural = "профили пользователей"

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class ProductCategory(models.Model):
    name = models.CharField(max_length=80, unique=True)
    photo = models.ImageField(upload_to='category_photos/', blank=True, null=True)

    class Meta:
        verbose_name = "Категория товара"
        verbose_name_plural = "Категории товаров"

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=150, unique=True)
    category = models.ForeignKey('ProductCategory', on_delete=models.PROTECT, related_name='products', verbose_name='Категория')
    unit = models.CharField(max_length=30, choices=[
        ('kg', 'кг'),
        ('t', 'т'),
        ('l', 'л'),
        ('pcs', 'шт'),
        ('dozen', 'дес'),
        ('pack', 'упак'),
    ], default='kg')
    price = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    description = models.TextField("Описание / сорт / особенности", blank=True)
    photo = models.ImageField(upload_to='product_photos/', blank=True, null=True)

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"

    def __str__(self):
        return f'{self.name} ({self.unit})'


class Order(models.Model):
    STATUS_CHOICES = [
        ('new', 'Новый'),
        ('processing', 'В обработке'),
        ('shipped', 'Отправлен'),
        ('delivered', 'Доставлен'),
        ('cancelled', 'Отменён'),
        ('returned', 'Возврат'),
    ]

    PAYMENT_CHOICES = [
        ('cash', 'Наличными при получении'),
        ('card', 'Картой онлайн'),
        ('upon_delivery', 'Картой при получении'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='orders',
        verbose_name='Клиент'
    )

    phone = models.CharField(
        max_length=20,
        blank=True,
        verbose_name='Телефон для связи'
    )

    # Если гость сделал заказ — сохраняем данные вручную
    guest_email = models.EmailField(blank=True, null=True, verbose_name='Email гостя')
    guest_phone = models.CharField(max_length=20, blank=True, null=True, verbose_name='Телефон гостя')
    guest_name = models.CharField(max_length=150, blank=True, null=True, verbose_name='Имя гостя')

    created_at = models.DateTimeField(default=timezone.now, verbose_name='Создан')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Обновлён')

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='new',
        verbose_name='Статус заказа'
    )

    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_CHOICES,
        default='cash',
        verbose_name='Способ оплаты'
    )

    total_price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
        verbose_name='Общая сумма'
    )

    delivery_address = models.TextField(blank=True, verbose_name='Адрес доставки')
    delivery_date = models.DateField(null=True, blank=True, verbose_name='Желаемая дата доставки')
    comment = models.TextField(blank=True, verbose_name='Комментарий к заказу')

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        if self.user:
            return f"Заказ #{self.id} — {self.user.email}"
        return f"Заказ #{self.id} (гость: {self.guest_email or self.guest_phone})"

    def calculate_total(self):
        total = sum(item.get_subtotal() for item in self.items.all())
        self.total_price = total
        self.save(update_fields=['total_price'])
        return total


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name='Заказ'
    )

    product = models.ForeignKey(
        'Product',
        on_delete=models.SET_NULL,
        null=True,
        related_name='order_items',
        verbose_name='Товар'
    )

    quantity = models.PositiveIntegerField(default=1, verbose_name='Количество')
    price_at_order = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Цена на момент заказа'
    )  # фиксируем цену, чтобы изменения не влияли на старые заказы

    manager = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='managed_orders',
        verbose_name='Ответственный менеджер'
    )

    # и желательно поле для отслеживания, кто последний раз менял статус
    last_modified_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='modified_orders',
        verbose_name='Последний редактор'
    )

    class Meta:
        verbose_name = 'Позиция заказа'
        verbose_name_plural = 'Позиции заказа'

    def __str__(self):
        return f"{self.quantity} × {self.product.name if self.product else 'Удалённый товар'}"

    def get_subtotal(self):
        return self.quantity * self.price_at_order