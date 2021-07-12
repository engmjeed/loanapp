from .models import Product
from rest_framework import generics
from utils.views import TransactionalViewMixin
from rest_framework.permissions import AllowAny
from rest_framework.decorators import(
	authentication_classes, 
	permission_classes
)
from .serializers import Productserializer

@permission_classes((AllowAny, ))
class ProductsViewSet(TransactionalViewMixin,generics.ListCreateAPIView,generics.RetrieveUpdateAPIView):
	""" this list transactions """

	serializer_class=Productserializer
	filterset_fields = ['name',]
	search_fields = ['name',]
	queryset =  Product.objects.all()
	

