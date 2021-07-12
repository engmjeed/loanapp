from .models import Fund
from rest_framework import generics
from utils.views import TransactionalViewMixin
from rest_framework.permissions import AllowAny
from rest_framework.decorators import(
	authentication_classes, 
	permission_classes
)
from .serializers import Fundserializer

@permission_classes((AllowAny, ))
class FundsViewSet(TransactionalViewMixin,generics.ListCreateAPIView):
	""" this list transactions """

	serializer_class=Fundserializer
	filterset_fields = ['name',]
	search_fields = ['name',]
	queryset = Fund.objects.all()

