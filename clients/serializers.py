from django.db import models
from rest_framework import serializers
from .models import Client,LoanProfile
from users.models import User
from phonenumber_field.serializerfields import PhoneNumberField

class Clientserializer(serializers.ModelSerializer):
    
    center = serializers.IntegerField(source='center_id')
    officer = serializers.PrimaryKeyRelatedField(queryset=User.objects.filter(is_staff=True))
    msisdn = PhoneNumberField()
    is_active = serializers.BooleanField(default=False)
    
    
    class Meta:
        model = Client
        fields = (
            'msisdn',
            'middle_name',
            'first_name',
            'last_name',
            'id_no',
            'is_active',
            'products',
            "officer",
            "center",
            "pin",
            )
        extra_kwargs = {'products': {'required': False}}

class ClientLoanProfileserializer(serializers.ModelSerializer):
    
    product = serializers.IntegerField(source='product_id')
    client = serializers.IntegerField(source='client_id')
    is_active = serializers.BooleanField(default=True)
    
    
    class Meta:
        model = LoanProfile
        fields = (
            'minimum_principle',
            'maximum_principle',
            'loan_limit',
            'product',
            "client",
            "is_active",
            
            )
    