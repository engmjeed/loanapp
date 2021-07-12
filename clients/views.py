from .models import Client,LoanProfile
from rest_framework import generics
from utils.views import TransactionalViewMixin
from rest_framework.permissions import AllowAny
from rest_framework.decorators import(
	authentication_classes, 
	permission_classes
)
from .serializers import Clientserializer,ClientLoanProfileserializer

@permission_classes((AllowAny, ))
class ClientsViewSet(TransactionalViewMixin,generics.ListCreateAPIView,generics.RetrieveUpdateAPIView):
	""" this list transactions """

	serializer_class=Clientserializer
	filterset_fields = ['msisdn',]
	search_fields = ['msisdn',]
	queryset =  Client.objects.all()



@permission_classes((AllowAny, ))
class ClientLoanProfilesViewSet(TransactionalViewMixin,generics.ListCreateAPIView,generics.RetrieveUpdateAPIView):
	""" this list transactions """

	serializer_class=ClientLoanProfileserializer
	filterset_fields = ['client__msisdn','product__id']
	search_fields = ['client__msisdn','product__id']
	queryset =  LoanProfile.objects.all()


