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

    def add(self, product, qty):
        product_id = str(product.id)
        if product_id not in self.basket:
            self.basket[product_id] = {'qty': qty, 'price': str(product.price)}
        self.basket[product_id]['qty'] = qty
        self.session.modified = True
