from django.db import models
from rest_framework import serializers
from .models import Fund

class Fundserializer(serializers.ModelSerializer):

    is_active = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = Fund
        fields = (
            'name',
            'description',
            'balance',
            'is_active',
            )