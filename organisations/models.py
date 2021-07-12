from django.db import models
from django.db.models import manager
from phonenumber_field.modelfields import PhoneNumberField
from factory.models import FactoryModel
from django.conf import settings
# Create your models here.

class Organisation(FactoryModel):

    name = models.CharField(max_length=50,unique=True)
    contact_email = models.EmailField()
    contact_phone = PhoneNumberField()
    address = models.CharField(max_length=100)
    manager = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING)
    is_active = models.BooleanField(default=False)
    products = models.ManyToManyField('products.Product')

    def __str__(self) -> str:
        return self.name

class Center(FactoryModel):

    name = models.CharField(max_length=50,unique=True)
    contact_email = models.EmailField()
    contact_phone = PhoneNumberField()
    address = models.CharField(max_length=100)
    organisation = models.ForeignKey(Organisation, on_delete=models.CASCADE,related_name='centers')
    manager = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING)
    is_active = models.BooleanField(default=False)
    products = models.ManyToManyField('products.Product')

    def __str__(self) -> str:
        return self.name

    