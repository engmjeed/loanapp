from .models import Charge
from rest_framework import generics
from utils.views import TransactionalViewMixin
from rest_framework.permissions import AllowAny
from rest_framework.decorators import(
	authentication_classes, 
	permission_classes
)
from .serializers import Chargeserializer

@permission_classes((AllowAny, ))
class ChargesViewSet(TransactionalViewMixin,generics.ListCreateAPIView):
	""" this list transactions """

	serializer_class=Chargeserializer
	filterset_fields = ['name',]
	search_fields = ['name',]
	queryset = Charge.objects.all()

