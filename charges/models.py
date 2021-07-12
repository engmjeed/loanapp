from django.db import models
from factory.models import FactoryModel
# Create your models here.

class Charge(FactoryModel):

    name = models.CharField(max_length=50,unique=True)
    description = models.CharField(max_length=100,null=True)
    amount = models.DecimalField(max_digits=7,decimal_places=2, default=0)
    is_active = models.BooleanField(default=True)

    def __str__(self) -> str:
        return self.name

