# from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from django.db import models

# class CustomUser(AbstractUser):
#     username = None
#     email = models.EmailField(unique=True)
#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = []

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

    def __str__(self):
        return f"Профиль {self.user.email or self.user.username}"

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

class CartItem(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='cart_items'
    )
    session_key = models.CharField(max_length=40, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = [
            ('user', 'product'),  # один товар — одна строка у авторизованного
            ('session_key', 'product'),  # то же для гостя
        ]
        verbose_name = "Позиция корзины"
        verbose_name_plural = "Позиции корзины"

    def __str__(self):
        who = self.user.email if self.user else f"гость ({self.session_key[:8]}…)"
        return f"{self.quantity} × {self.product.name} ({who})"

    @property
    def total_price(self):
        if self.product.price is None:
            return 0
        return self.quantity * self.product.price