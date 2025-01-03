from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from django_email_verification import urls as email_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('shop/', include('shop.urls', namespace='shop')),
    path('basket/', include('basket.urls', namespace='basket')),
    path('account/', include('account.urls', namespace='account')),
    path('payment/', include('payment.urls', namespace='payment')),
    path('email/', include(email_urls), name='email_verification_sent'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)