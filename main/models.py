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
        verbose_name = "профиль"
        verbose_name_plural = "профили"

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

class ProductCategory(models.Model):
    name = models.CharField(max_length=80, unique=True)

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

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
        ('l_day', 'л/сут'),  # для суточного надоя молока
        ('pack', 'упак'),
    ], default='kg')
    price = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    is_animal = models.BooleanField("Продукция животноводства", default=False)
    description = models.TextField("Описание / сорт / особенности", blank=True)

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"

    def __str__(self):
        return f'{self.name} ({self.unit})'