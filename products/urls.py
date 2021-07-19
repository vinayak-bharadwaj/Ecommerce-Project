from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.product_home.as_view(), name = "product-home"),
    path('AddCart/<int:pk>', views.add_cart  ,name = "add-cart"),
    path('RemoveCart/<int:pk>', views.remove_cart  ,name = "remove-cart"),
    path('Cart', views.CartListView.as_view()  ,name = "cart"),
    path('Orders', views.OrderListView.as_view(), name="orders")    
]

if settings.DEBUG:
	urlpatterns+= static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)