from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse

from basket.basket import Basket
from shop.models import ProductProxy

def basket_view(request):
    basket = Basket(request)
    context = {'basket': basket}
    return render(request, 'basket/basket-view.html', context)

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
    basket = Basket(request)

    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        basket.delete(product=product_id)
        basket_qty = basket.__len__()
        basket_total = basket.get_total_price()
        response = JsonResponse({'qty': basket_qty, 'total': basket_total})
        return response

def basket_update(request):
    basket = Basket(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        print(product_id)
        print(request.POST.get('product_qty'))
        print('======')
        product_qty = int(request.POST.get('product_qty'))
        print(product_qty)
        basket.update(product=product_id, quantity=product_qty)
        basket_qty = basket.__len__()
        basket_total = basket.get_total_price()
        response = JsonResponse({'qty': basket_qty, 'total': basket_total})
        return response