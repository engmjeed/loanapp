from django.db import models
from factory.models import FactoryModel
from flex.ussd.utils import AttributeBag

# Create your models here.

class Account(FactoryModel):

    number = models.CharField(max_length=10)
    client = models.OneToOneField('clients.Client', on_delete=models.PROTECT)
    product = models.ForeignKey('products.Product',on_delete=models.DO_NOTHING)
    balance = models.DecimalField(max_digits=8, decimal_places=2,default=0)
    
    def save(self, *args, **kwargs):
        self.number = str(self.pk).zfill(9)
        super(Account, self).save(*args, **kwargs)
    def __str__(self) -> str:
        return self.number
