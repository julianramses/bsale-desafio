# bsale-desafio
Parte del backend del desafío bsale, se nos otorga una base de datos con la cual hay que crear una API REST, la cual luego será consumida en una aplicación front end, utilizando Javascript vanilla.

nos conectamos a la base de datos declarando lo siguiente

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'USER': 'bsale_test',
        'NAME': 'bsale_test',
        'HOST':'mdb-test.c6vunyturrl6.us-west-1.rds.amazonaws.com',
        'PORT': '3306',
        'PASSWORD': 'bsale_test',
        'OPTIONS' : {
            'init_command' : "SET sql_mode = 'STRICT_TRANS_TABLES'" 
        }
    }
        
}
````
extraemos los datos de la base de datos mediante 
inspectdb

`$ python manage.py inspectdb > models.py`

lo que nos crea nuestros modelos
```python
# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'category'


class Product(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    url_image = models.CharField(max_length=255, blank=True, null=True)
    price = models.FloatField(blank=True, null=True)
    discount = models.IntegerField(blank=True, null=True)
    category = models.ForeignKey(Category, models.DO_NOTHING, db_column='category', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'product'

````
Con los datos extraidos, podemos empezar a trabajar en la api.

en nuestras views.py creamos lo siguiente
```python
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

````
Imports como method_decorator, csrf_exempt no fueron necesarios, ya que la base de datos es read only, por lo cual la api solo tiene funcion GET.
PUT,POST,DELETE no estan disponibles por motivos de permisos.

Para verificar que la API esta funcionando, debemos utilizar alguna herramienta para generar un request, 
## API Reference

#### GET de todos los productos y los atributos

```http
  GET /productos/productos/
```
lo que nos da como respuesta todos los productos.
```json
"{
	"message": "Success",
	"productos": [{
		"id": 5,
		"name": "ENERGETICA MR BIG",
		"url_image": "https://dojiw2m9tvv09.cloudfront.net/11132/product/misterbig3308256.jpg",
		"price": 1490.0,
		"discount": 20,
		"category_id": 1
	}, {
		"id": 6,
		"name": "ENERGETICA RED BULL",
		"url_image": "https://dojiw2m9tvv09.cloudfront.net/11132/product/redbull8381.jpg",
		"price": 1490.0,
		"discount": 0,
		"category_id": 1
	}, {
  ....
`````

#### GET de un producto en especifico por id
```http
  GET /productos/productos/5
```
lo que nos da como respuesta el primer producto de id 5.
```json
{
	"message": "Success",
	"productos": [{
		"id": 5,
		"name": "ENERGETICA MR BIG",
		"url_image": "https://dojiw2m9tvv09.cloudfront.net/11132/product/misterbig3308256.jpg",
		"price": 1490.0,
		"discount": 20,
		"category_id": 1
	}]
}
````
mensaje de error (id no existe)

```json
{"message": "Not found"}
````

esto aplica también para las categorías
```http
GET /productos/category/
````
```json
  {
 	"message": "Success",
 	"category": [{
 		"id": 1,
 		"name": "bebida energetica"
 	}, {
 		"id": 2,
 		"name": "pisco"
 	}, {
 		"id": 3,
 		"name": "ron"
 	}, {
 		"id": 4,
 		"name": "bebida"
 	}, {
 		"id": 5,
 		"name": "snack"
 	}, {
 		"id": 6,
 		"name": "cerveza"
 	}, {
 		"id": 7,
 		"name": "vodka"
 	}]
 }
````

```http
GET /productos/category/1
````
```json
{
	"message": "Success",
	"category": [{
		"id": 1,
		"name": "bebida energetica"
	}]
}
````
De esta manera, podemos trabajar con la API REST
