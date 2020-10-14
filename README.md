# TEST SAVOLA :))


#####test_1 || Shu modelga CRUD qlish kere `djangorestframework` ishlatib va test yozish kere
```python
from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=57)
    price = models.IntegerField(default=0)
```

#####test_2 || Shu modelan `Acer` db boshlangan xamma productlani select qb chiqarish kerak
```python
from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=57)
    price = models.IntegerField(default=0)
```
#####test_3 || Manga Productla qancha sotilganini soni kerak va nech puligi.
`Order status finish` bolganlarini xisoblash kerak `SubQuery` orqali
```python
from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=57)
    price = models.IntegerField(default=0)


class Order(models.Model):
    NEW = 'new'
    FINISH = 'finish'
    STATUS = ((NEW,NEW),(FINISH,FINISH))
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    count = models.IntegerField(default=1)
    status = models.CharField(choices=STATUS, default=NEW, max_length=25)
```

#####test_4 || Manga shu view faqat kevotgan user admin bolsagina ishlasin
```python
from rest_framework.views import APIView, Response

class FooView(APIView):
    def get(self, request):
        return Response({"message":"HELLO ADMIN"})
        
    def post(self, request):
        return Response({"message":"HELLO ADMIN"})
        
    def put(self, request):
        return Response({"message":"HELLO ADMIN"})
```

#####test_5 || Shu serializerga `custom_obj` method field qilib qoshish kerak
```python
from django.db import models
from rest_framework import serializers

class Product(models.Model):
    name = models.CharField(max_length=57)
    price = models.IntegerField(default=0)

custom_obj = {'foo': 'bar'}


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'price']
    
```
Shunaqa korinishda chiqish kerak
```json
{
  "id": 1,
  "name": "Acer",
  "price": 500,
  "custom": {"foo": "bar"}
}
```
