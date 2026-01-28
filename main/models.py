from django.db import models

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