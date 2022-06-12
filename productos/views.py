import http
from itertools import product
from unicodedata import category, name
from django.shortcuts import render
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import json
import productos
from .models import Product, Category
from django.views import View
from django.http.response import JsonResponse


class ProductView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):#NO APLICA, BASE DE DATOS READ ONLY.
        return super().dispatch(request, *args, **kwargs)

    def get (self,request, id=0):
        if (id>0):
            productos=list(Product.objects.filter(id=id).values())
            if len(productos)>0:
                datos={'message':'Success','productos':productos}
            else:
                datos={'message':'Not found'}
            return JsonResponse(datos)
        else:
            productos=list(Product.objects.values())
            if len(productos)>0:
                datos={'message':'Success','productos':productos}
            else:
                datos={'message':'Not found'}
            return JsonResponse(datos)

    def post(self,request):#NO APLICA, BASE DE DATOS READ ONLY.
        jd = json.loads(request.body)
        print(jd)
        Product.objects.create(id=jd['id'],name=jd['name'],url_image=jd['url_image'], price=jd['price'], discount=jd['discount'], category_id=jd['category_id'])
        datos={'message':'Success'}
        return JsonResponse(datos)
    def put (self,request): #NO APLICA, BASE DE DATOS READ ONLY.
        pass
    def delete (self,request):#NO APLICA, BASE DE DATOS READ ONLY.
        pass

class CategoryView(View):
    def get(self,request,id=0):
        if (id>0):
            category=list(Category.objects.filter(id=id).values())
            if len(category)>0:
                datos={'message':'Success','category':category}
            else:
                datos={'message':'Not found'}
            return JsonResponse(datos)
        else:
            category=list(Category.objects.values())
            if len(category)>0:
                datos={'message':'Success','category':category}
            else:
                datos={'message':'Not found'}
            return JsonResponse(datos)

