from django.urls import path, include
from . import views 
from .views import CategoryView, ProductView

urlpatterns = [
    path('productos/', ProductView.as_view(), name='productos_list'),
    path('productos/<int:id>', ProductView.as_view(), name='productos_process'),
    path('category/', CategoryView.as_view(), name='category_list'),
    path('category/<int:id>', CategoryView.as_view(), name='category_process'),
    ]