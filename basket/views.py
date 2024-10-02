from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse

from basket.basket import Basket
from shop.models import ProductProxy

def basket_view(request):
    return render(request, 'basket/basket-view.html')

def basket_add(request):
    basket = Basket(request)

    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        product_qty = int(request.POST.get('product_qty'))

        product = get_object_or_404(ProductProxy, id=product_id)

        basket.add(product=product, qty=product_qty)
        basket_qty = basket.__len__()
        response = JsonResponse({'qty': basket_qty, 'product': product.title})

        return response

def basket_delete(request):
    pass

def basket_update(request):
    pass