from django.db import models
from rest_framework import serializers
from .models import Application,Loan

class LoanSerializer(serializers.ModelSerializer):

    class Meta:
        model = Loan
        fields = ('__all__')

class LoanApplicationSerializer(serializers.ModelSerializer):

    client = serializers.IntegerField(source='client_id')
    product = serializers.IntegerField(source='product_id')

   
    
    class Meta:
        model = Application
        fields = (
            'client',
            'product',
            'amount',
            'duration',
            )
