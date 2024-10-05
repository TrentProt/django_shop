from django.urls import path
from .views import basket_view, basket_add, basket_delete, basket_update


app_name = 'basket'

urlpatterns = [
    path('', basket_view, name='basket'),
    path('add/', basket_add, name='add_to_basket'),
    path('delete/', basket_delete, name='delete_from_basket'),
    path('update/', basket_update, name='update_basket')
]