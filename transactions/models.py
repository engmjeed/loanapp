from django.db import models
from django.db.models.deletion import CASCADE, PROTECT
from factory.models import FactoryModel, QuerySet, Manager
from django_enumfield import enum
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.utils import timezone

# Create your models here.

class TransactionTypeEnum(enum.Enum):

    DEBIT = 1
    CREDIT = 2

class TransactionQuerySet(QuerySet):
    def filter_by_type(self):
        typ = self.model.__type__
        return self if typ is None else self.filter(type=typ)


class TransactionManager(Manager.from_queryset(TransactionQuerySet)):
    def get_queryset(self):
        return super().get_queryset().filter_by_type()

    

class Transaction(FactoryModel):

    __type__ = None

    Type = TransactionTypeEnum

    objects = TransactionManager()

    class Meta:
        # abstract = True
        verbose_name = "transaction"
        verbose_name_plural = "transactions"
        ordering = ["-created_at"]

    client = models.ForeignKey('clients.Client',on_delete=models.CASCADE,related_name='transactions')
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE)
    type = enum.EnumField(Type)
    subject = models.CharField(max_length=128)

    amount = models.DecimalField(max_digits=12, decimal_places=2)
    initial_balance = models.DecimalField(max_digits=12, decimal_places=2)

    details = models.CharField(max_length=255, default="")

    timestamp = models.DateTimeField(default=timezone.now)

    ref_type = models.ForeignKey(ContentType, null=True, on_delete=models.DO_NOTHING)
    ref_id = models.CharField(max_length=128, null=True)
    ref = GenericForeignKey("ref_type", "ref_id")

    @property
    def final_balance(self):
        return self.initial_balance + self.value

    @property
    def value(self):
        if self.type == self.Type.CREDIT:
            return self.amount
        else:
            return self.amount * -1

    def __init__(self, *args, **kw):
        args or kw.setdefault("type", self.__type__)
        super().__init__(*args, **kw)

    def __str__(self):
        return str(self.ref_id)

