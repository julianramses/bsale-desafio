from django.urls import path, include
from . import views 
from .views import ProductView, Category

urlpatterns = [
    path('productos/', ProductView.as_view(), name='productos_list')
]