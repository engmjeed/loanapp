from typing import Tuple
from django.db import models
from factory.models import FactoryModel
from django_enumfield import enum
from django.utils import timezone

# Create your models here.



class PayInStatusEnum(enum.Enum):
    
    PENDING = 0
    PROCESSED = 1
    ERRORED = 2
    __default__ = PENDING

class PayOutStatusEnum(enum.Enum):
    
    PENDING = 0
    PROCESSED = 1
    ERRORED = 2
    __default__ = PENDING

class CheckOutStatusEnum(enum.Enum):
    
    PENDING = 0
    PROCESSED = 1
    ERRORED = 2
    __default__ = PENDING


class PayIn(FactoryModel):
    
    client = models.ForeignKey('clients.Client', on_delete=models.DO_NOTHING)
    loan = models.ForeignKey('loans.Loan',on_delete=models.DO_NOTHING,null=True)
    amount = models.DecimalField(max_digits=8,decimal_places=2)
    mpesa_code = models.CharField(max_length=10)
    bill_ref_no = models.CharField(max_length=10,null=True,blank=True)
    transaction_date = models.DateTimeField() 
    status = enum.EnumField(PayInStatusEnum)
    notes = models.CharField(max_length=50)
    raw = models.JSONField()

    @classmethod
    def get_unprocessed(cls,limit):
        return cls.objects.filter(status=PayInStatusEnum.default()).exclude(loan__isnull=True).order_by('id')[:limit]


class PayOut(FactoryModel):
    
    loan = models.OneToOneField('loans.Loan', on_delete=models.DO_NOTHING)
    amount =models.DecimalField(max_digits=7,decimal_places=2)
    receipient_phone = models.CharField(max_length=13)
    status = enum.EnumField(PayOutStatusEnum)
    notes = models.CharField(max_length=50)
    mpesa_code = models.CharField(max_length=10,null=True)
    results = models.JSONField(default=dict)

    def __str__(self) -> str:
        return self.receipient_phone + ' #' + str(self.amount)

    @classmethod
    def get_unprocessed(cls,limit):
        return cls.objects.filter(status=PayOutStatusEnum.default()).order_by('id')[:limit]



    @classmethod
    def create(cls,loan):
        amount = loan.application.amount
        receipient_phone = str(loan.application.client.msisdn).strip('+').strip()
        return cls.objects.create(loan=loan,amount=amount,receipient_phone=receipient_phone)
class Checkout(FactoryModel):
    
    amount = models.DecimalField(max_digits=7,decimal_places=2)
    ref_no = models.IntegerField()
    msisdn = models.CharField(max_length=13)
    status = enum.EnumField(CheckOutStatusEnum)
    notes = models.TextField(null=True)
    @classmethod
    def get_unprocessed(cls,limit):
        return cls.objects.filter(status=CheckOutStatusEnum.default()).order_by('id')[:limit]




