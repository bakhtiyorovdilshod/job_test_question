# 1-savol

# views.py
from rest_framework import viewsets
from .models import  Product
from .serializers import ProductSerializer
from rest_framework.response import Response
from django.db.models import Subquery

class ProductModelViewSet(viewsets.ModelViewSet):
	queryset = Product.objects.all()
	serializer_class = ProductSerializer



# override  qilsak buladi CRUD larni t=tepadagi class ga pastdagi largi qushib.
 # def list(self, request):
 #        pass

 #    def create(self, request):
 #        pass

 #    def retrieve(self, request, pk=None):
 #        pass

 #    def update(self, request, pk=None):
 #        pass

 #    def partial_update(self, request, pk=None):
 #        pass

 #    def destroy(self, request, pk=None):
 #        pass

# urls.py 

from django.urls import path, include
from rest_framework.routers import SimpleRouter
from .views import ProductModelViewSet
from rest_framework.permissions import IsAuthenticated, IsAdminUser

router = SimpleRouter()
router.register('', ProductModelViewSet)



urlpatterns = [
    path('', include(router.urls)),
    
]


# Testing

from django.test import TestCase
from .models import Product


class ProductTest(TestCase):
    """ 
    Test module for Product model 
    """

    def product_create(self):
        Product.objects.create(
            name='ACER', price=200)
        Product.objects.create(
            name='ASUS', price=300)

    def test_product(self):
        product_one = Product.objects.get(name='ACER')
        product_two = Product.objects.get(name='ASUS')
        self.assertEqual(
            product_one.name, "ACER")
        self.assertEqual(
            product_two.name, "ASUS")


# test_views.py

from rest_framework import status
from django.test import TestCase, Client
from django.urls import reverse
from .serializers import  ProductSerializer

class GetALLProductsTest(TestCase):

    def product_create(self):
        Product.objects.create(name='ACER', price=200)
        Product.objects.create(name='ASUS', price=300)


    def test_all_products(self):
    	response = client.get(reverse('all products'))
    	products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)



class OneProductTest(TestCase):

	def product_create(self):
        self.product_one = Product.objects.create(name='ACER', price=200)
        self.product_two = Product.objects.create(name='ASUS', price=300)

    def test_get_valid_product(self):
        response = client.get(
            reverse('get product', kwargs={'pk': self.product_one.pk}))
        product = Product.objects.get(pk=self.product_one.pk)
        serializer = ProductSerializer(product)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_invalid_product(self):
        response = client.get(
            reverse('get product', kwargs={'pk': 2}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)



class CreateProductTest(TestCase):
    def setUp(self):
        self.valid_product = {
            'name': 'ACER',
            'price':200
        }
        self.invalid_product = {
            'name': 'ASUS',
            'price':0
  
        }

    def test_create_valid_product(self):
        response = client.post(
            reverse('post product'),
            data=json.dumps(self.valid_product),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_product(self):
        response = client.post(
            reverse('post product'),
            data=json.dumps(self.invalid_product),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)



class EditProductTest(TestCase):

	def product_create(self):
        self.product_one = Product.objects.create(name='ACER', price=200)
        self.product_two = Product.objects.create(name='ASUS', price=300)

        self.valid_product = {
            'name': 'ACER',
            'price':200
        }
        self.invalid_product = {
            'name': 'ASUS',
            'price':0
  
        }

    def test_valid_edit_product(self):
        response = client.put(
            reverse('edit product', kwargs={'pk': self.product_one.pk}),
            data=json.dumps(self.valid_product),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_invalid_edit_product(self):
        response = client.put(
            reverse('edit product', kwargs={'pk': self.product_one.pk}),
            data=json.dumps(self.invalid_product),
            content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class DeleteOneProductTest(TestCase):

    def product_create(self):
        self.product_one = Product.objects.create(name='ACER', price=200)
        self.product_two = Product.objects.create(name='ASUS', price=300)

    def test_valid_delete_product(self):
        response = client.delete(
            reverse('delete product', kwargs={'pk': self.product_one.pk}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_invalid_delete_product(self):
        response = client.delete(
            reverse('delete product', kwargs={'pk': 30}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)








# 2-savol
def get_acer_product(self):
	products = Product.objects.filter(name='Acer')
	serializer = ProductSerializer(products, many=True)
	return Respone(serializer.data)


# 3-savol


class OrderSerializer(serializers.ModelSerializer):
	product = ProductSerializer(many=False, read_only=True)
	class Meta:
		model = Order
		fields = ['count', 'product']
products = Product.objects.all()
orders = Order.objects.filter(status= 'finish', product_id__in=Subquery(products.values('id')))
serializer = OrderSerializer(orders, many=True)
return Response(serializer.data)

{
	{
		"count":100,
		"product":{
			"price":50 # bu yerdan priceni olsa buladi.
		}
	}
}


# 4-savol

# 1-yoli
class FooView(APIView):
	permission_classes = [IsAdminUser]
    def get(self, request):
        return Response({"message":"HELLO ADMIN"})
        
    def post(self, request):
        return Response({"message":"HELLO ADMIN"})
        
    def put(self, request):
        return Response({"message":"HELLO ADMIN"})

# 2-yoli

class FooView(APIView):
    def get(self, request):
    	if request.user.is_superuser:
    		return Response({"message":"HELLO ADMIN"})
    	else:
    		return Response('You do not have permission in this endpoint')
        
    def post(self, request):
        if request.user.is_superuser:
    		return Response({"message":"HELLO ADMIN"})
    	else:
    		return Response('You do not have permission in this endpoint')
        
    def put(self, request):
        if request.user.is_superuser:
    		return Response({"message":"HELLO ADMIN"})
    	else:
    		return Response('You do not have permission in this endpoint')

# 5-savol

from django.db import models
from rest_framework import serializers


class Product(models.Model):
    name = models.CharField(max_length=57)
    price = models.IntegerField(default=0)

    @property
    def custom_obj(self):
    	data = {'foo': 'bar'}
        return data




class ProductSerializer(serializers.ModelSerializer):
	my_field = serializers.ReadOnlyField(source='custom_obj')
    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'custom_obj']







