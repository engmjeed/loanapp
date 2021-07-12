from .models import Application,Loan
from rest_framework import generics
from utils.views import TransactionalViewMixin
from rest_framework.permissions import AllowAny
from rest_framework.decorators import(
	authentication_classes, 
	permission_classes
)
from .serializers import LoanApplicationSerializer,LoanSerializer

@permission_classes((AllowAny, ))
class LoanViewSet(TransactionalViewMixin,generics.ListAPIView,generics.RetrieveUpdateAPIView):
	""" this list transactions """

	serializer_class=LoanSerializer
	filterset_fields = ['client__msisdn','client__id']
	search_fields = ['client__msisdn','client__id']
	queryset =  Loan.objects.all()

@permission_classes((AllowAny, ))
class LoanApplicationsViewSet(TransactionalViewMixin,generics.ListCreateAPIView,generics.RetrieveUpdateAPIView):
	""" this list transactions """

	serializer_class=LoanApplicationSerializer
	filterset_fields = ['client__msisdn','client__id']
	search_fields = ['client__msisdn','client__id']
	queryset =  Application.objects.all()