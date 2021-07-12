from django.db import models
from django.db.models.deletion import PROTECT
from factory.models import FactoryModel
from django_enumfield import enum

# Create your models here.

class TransactionTypeEnum(enum.Enum):

    DEBIT = 1
    CREDIT = 2
    REVERSAL = 3
    OTHER = 4

class Transaction(FactoryModel):

    client = models.ForeignKey('clients.Client',on_delete=PROTECT)
    initial_balance = models.DecimalField(max_digits=8,decimal_places=2,default=0)
    final_balance = models.DecimalField(max_digits=8,decimal_places=2,default=0)
    amount = models.DecimalField(max_digits=9,decimal_places=2,default=0)
    description = models.CharField(max_length=50)
    ref_id = models.CharField(max_length=10)
    type = enum.EnumField(TransactionTypeEnum)
