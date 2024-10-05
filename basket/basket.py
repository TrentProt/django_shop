from decimal import Decimal

from shop.models import ProductProxy

class Basket():
    def __init__(self, request):
        self.session = request.session
        basket = self.session.get('session_key')
        if not basket:
            basket = self.session['session_key'] = {}
        self.basket = basket

    def __len__(self):
        return sum(item['qty'] for item in self.basket.values())

    def __iter__(self):
        product_ids = self.basket.keys()
        products = ProductProxy.objects.filter(id__in=product_ids)
        basket = self.basket.copy()
        print(products)
        for product in products:
            print(product)
            print(basket[str(product.id)])
            basket[str(product.id)]['product'] = product
        for item in basket.values():
            item['price'] = Decimal(item['price'])
            item['total'] = item['price'] * item['qty']
            yield item

    def add(self, product, qty):
        product_id = str(product.id)
        if product_id not in self.basket:
            self.basket[product_id] = {'qty': qty, 'price': str(product.price)}
        self.basket[product_id]['qty'] = qty
        self.session.modified = True

    def get_total_price(self):
        return sum(Decimal(item['price']) * item['qty'] for item in self.basket.values())

    def delete(self, product):
        product_id = str(product)
        if product_id in self.basket:
            print(self.basket)
            print(self.basket[product_id])
            del self.basket[product_id]
            self.session.modified = True

    def update(self, product, quantity):
        product_id = str(product)
        if product_id in self.basket:
            print(self.basket)
            print(self.basket[product_id])
            self.basket[product_id]['qty'] = quantity
            self.session.modified = True