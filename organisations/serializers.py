from django.db import models
from rest_framework import serializers
from .models import Organisation,Center
from phonenumber_field.serializerfields import PhoneNumberField

class Organisationserializer(serializers.ModelSerializer):
    
    manager = serializers.IntegerField(source='manager_id')
    contact_phone = PhoneNumberField()
    
    class Meta:
        model = Organisation
        fields = (
            'name',
            'contact_email',
            'contact_phone',
            'address',
            'manager',
            'is_active',
            'products',
            )
        extra_kwargs = {'products': {'required': False}}

class Centerserializer(serializers.ModelSerializer):
    
    manager = serializers.IntegerField(source='manager_id')
    contact_phone = PhoneNumberField()
    organisation = serializers.IntegerField(source='organisation_id')
    
    class Meta:
        model = Center
        fields = (
            'name',
            'contact_email',
            'contact_phone',
            'address',
            'manager',
            'is_active',
            'organisation',
            'products',
            )
        extra_kwargs = {'products': {'required': False}}
    
