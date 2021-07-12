from django.db import models
from rest_framework import serializers
from .models import Charge

class Chargeserializer(serializers.ModelSerializer):

    is_active = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = Charge
        fields = (
            'name',
            'description',
            'amount',
            'is_active',
            )