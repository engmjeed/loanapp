from .models import Organisation,Center
from rest_framework import generics
from utils.views import TransactionalViewMixin
from rest_framework.permissions import AllowAny
from rest_framework.decorators import(
	authentication_classes, 
	permission_classes
)
from .serializers import Organisationserializer,Centerserializer

@permission_classes((AllowAny, ))
class OrganisationsViewSet(TransactionalViewMixin,generics.ListCreateAPIView,generics.RetrieveUpdateAPIView):
	""" this list transactions """

	serializer_class=Organisationserializer
	filterset_fields = ['name',]
	search_fields = ['name',]
	queryset =  Organisation.objects.all()

@permission_classes((AllowAny, ))
class CentersViewSet(TransactionalViewMixin,generics.ListCreateAPIView,generics.RetrieveUpdateAPIView):
	""" this list transactions """

	serializer_class=Centerserializer
	filterset_fields = ['name',]
	search_fields = ['name',]
	queryset =  Center.objects.all()
	

