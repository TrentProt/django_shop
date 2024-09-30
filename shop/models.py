import random
import string

from django.db import models
from django.utils.text import slugify
import random
import string
from django.urls import reverse

def rand_slug():
    return ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(3))


class Category(models.Model):
    name = models.CharField(max_length=250, db_index=True, verbose_name='Название')
    parent = models.ForeignKey(
        'self', on_delete=models.CASCADE, related_name='children', blank=True, null=True, verbose_name='Родитель'
    )
    slug = models.SlugField(max_length=250, unique=True, null=False, editable=True, verbose_name='Слаг')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    class Meta:
        unique_together = (['slug', 'parent'])
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        full_path = [self.name]
        k = self.parent
        while k is not None:
            full_path.append(k.name)
            k = k.parent
        return ' > '.join(full_path[::-1])

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(rand_slug() + '-pickBetter' + self.name)
        super(Category, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('shop:category_list', args=[str(self.slug)])

class Product(models.Model):
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name='products', verbose_name='Категория'
    )
    title = models.CharField('Название', max_length=250)
    brand = models.CharField('Бренд', max_length=250)
    description = models.TextField('Описание', blank=True)
    slug = models.SlugField('Слаг', max_length=250)
    price = models.DecimalField('Цена', max_digits=7, decimal_places=2, default=99.99)
    image = models.ImageField('Изображение', upload_to='products/products/%Y/%m/%d')
    available = models.BooleanField('Наличие', default=True)
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField('Дата изменения', auto_now=True)

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('shop:product_detail', args=[str(self.slug)])

class ProductManager(models.Manager):

    def get_queryset(self):
        return super(ProductManager, self).get_queryset().filter(available=True)


class ProductProxy(Product):

    objects = ProductManager()

    class Meta:
        proxy = True