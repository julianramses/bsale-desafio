import http
from itertools import product
from django.shortcuts import render
from django.http import HttpResponse
from .models import Product, Category

def index(request):
    product = Product.objects.all()
    output = '<br>'.join([p.name for p in product])
    return HttpResponse(output)


# Create your views here.
