from django.db import models
from rest_framework import serializers
from .models import Product

class Productserializer(serializers.ModelSerializer):
    
    fund = serializers.IntegerField(source='fund_id')
    
    class Meta:
        model = Product
        fields = (
            'name',
            'short_name',
            'description',
            'minimum_principal',
            'maximum_principal',
            'interest_rate',
            'max_repayment_months',
            'fund',
            'charges',
            )
        extra_kwargs = {'charges': {'required': False}}
    
