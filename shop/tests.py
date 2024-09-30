from distutils.command.upload import upload

from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse

from .models import Product, Category, ProductProxy

class ProductViewTest(TestCase):
    def test_get_products(self):
        small_gif = (
            b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x00\x00\x00\x21\xf9\x04'
            b'\x01\x0a\x00\x01\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02'
            b'\x02\x4c\x01\x00\x3b'
        )
        uploaded = SimpleUploadedFile('test_image.gif', small_gif, content_type='image/gif')
        print(uploaded)
        category = Category.objects.create(name='django')
        print(category)
        product_1 = Product.objects.create(title='Product 1', category=category, image=uploaded, slug='product-1')
        print(product_1)
        product_2 = Product.objects.create(title='Product 2', category=category, image=uploaded, slug='product-2')
        print(product_2)
        response = self.client.get(reverse('shop:products'))
        print(response)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['products'].count(), 2)
        print(response.context['products'])
        self.assertEqual(list(response.context['products']), [product_1, product_2])
        self.assertContains(response, product_1)
        self.assertContains(response, product_2)

