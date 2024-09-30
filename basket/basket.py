from decimal import Decimal

from shop.models import ProductProxy

class Basket():
    def __init__(self, request):
        self.session = request.session
