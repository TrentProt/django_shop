import json

from django.contrib.sessions.middleware import SessionMiddleware

from django.test import Client, RequestFactory, TestCase
from django.urls import reverse

from shop.models import Category, ProductProxy

from .views import basket_add, basket_view

class BasketvView(TestCase):

    def setUp(self):
        self.client = Client()
        self.factory = RequestFactory().get(reverse('basket:basket'))
        self.middleware = SessionMiddleware(self.factory)
        self.middleware.process_request(self.factory)
        self.factory.session.save()

    def test_basket_view(self):
        request = self.factory
        response = basket_view(request)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(self.client.get(reverse('basket:basket')), 'basket/basket-view.html')

class CardAddViewTestCase(TestCase):

    def setUp(self):
        self.category = Category.objects.create(name='Category 1')
        self.product = ProductProxy.objects.create(title='Prod 1', price=10.0, category=self.category)
        self.factory = RequestFactory().post(reverse('basket:add_to_basket'), {
            'action': 'post',
            'product_id': self.product.id,
            'product_qty': 2
        })
        self.middleware = SessionMiddleware(self.factory)
        self.middleware.process_request(self.factory)
        self.factory.session.save()

    def test_card_add(self):
        request = self.factory
        response = basket_add(request)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data['product'], 'Prod 1')
        self.assertEqual(data['qty'], 2)


