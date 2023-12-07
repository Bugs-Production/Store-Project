from django.db import models

from users.models import User


# Create your models here.
class ProductCategory(models.Model):
    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'

    name = models.CharField('Название категории', max_length=128)
    description = models.TextField('Описание категории', blank=True, null=True)

    def __str__(self):
        return f'Категория - {self.name}'


class Product(models.Model):
    class Meta:
        verbose_name = 'товар'
        verbose_name_plural = 'Товары'

    name = models.CharField('Наименование товара', max_length=128)
    description = models.TextField('Описание товара')
    price = models.DecimalField('Цена', max_digits=12, decimal_places=2)
    quantity = models.PositiveIntegerField('Количество товара', default=0)
    image = models.ImageField('Картинка для товара', upload_to='products_images')
    category = models.ForeignKey(to=ProductCategory, on_delete=models.CASCADE, verbose_name='Категория товара')

    def __str__(self):
        return f'Товар - {self.name} | {self.category}'


class BasketMethod(models.QuerySet):  # Создание методов для подсчета суммы и количества товаров
    def total_sum(self):
        return sum(basket.sum() for basket in self)

    def total_quantity(self):
        return sum(basket.quantity for basket in self)


class Basket(models.Model):
    class Meta:
        verbose_name = 'корзина'
        verbose_name_plural = 'Корзина'

    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(default=0)
    created_timestamp = models.DateTimeField(auto_now_add=True)

    objects = BasketMethod.as_manager()

    def sum(self):
        return self.quantity * self.product.price

    def __str__(self):
        return f'Корзина для {self.user.username} | товар - {self.product.name}'
