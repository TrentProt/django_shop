from django.urls import path
from .views import basket_view, basket_add, basket_delete, basket_update


app_name = 'basket'

urlpatterns = [
    path('', basket_view, name='basket'),
    path('add/', basket_add, name='add_to_basket'),
    # path('search/<slug:slug>/', category_list, name='category_list'),
]