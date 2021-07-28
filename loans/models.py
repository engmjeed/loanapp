from django.db import models
from factory.models import FactoryModel
from django.conf import settings
from django_enumfield import enum
from django.utils import timezone
import uuid

# Create your models here.

def gen_ref_no():
    return uuid.uuid4().hex


class ApplicationStatusEnum(enum.Enum):
    
    PENDING = 0
    APPROVED = 1
    REJECTED = 2
    PROCESSED = 3
    FAILED = 4
    __default__ = PENDING
    
    __transitions__ = {
        APPROVED: (PENDING,REJECTED),  # Can go from PENDING,REJECTED to APPROVED
        REJECTED: (PENDING,),  # Can go from PENDING to REJECTED
        FAILED: (PENDING,APPROVED),  # Can go from PENDING to REJECTED
        PENDING: (FAILED,),  # Can go from PENDING to REJECTED
        PROCESSED: (APPROVED,),  # Can go from APPROVED to PROCESSED

    }

class Application(FactoryModel):
    
    client = models.ForeignKey('clients.Client',on_delete=models.DO_NOTHING)
    ref_no = models.CharField(max_length=32,default=gen_ref_no)
    product = models.ForeignKey('products.Product',on_delete=models.DO_NOTHING)
    amount = models.DecimalField(max_digits=7,decimal_places=2)
    status = enum.EnumField(ApplicationStatusEnum)
    notes = models.CharField(max_length=50,null=True,blank=True)
    duration = models.IntegerField()
    code = models.BigIntegerField()
    reviewed_by =models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING,null=True,blank=True)

    def __str__(self) -> str:
        return self.client.first_name +':-' + str(self.product.name) 

    @classmethod
    def get_unprocessed(cls,limit):
        return cls.objects.filter(status=ApplicationStatusEnum.APPROVED).order_by('id')[:limit]



class Loan(FactoryModel):

    application = models.OneToOneField(Application, on_delete=models.PROTECT,related_name='loan')
    date_due = models.DateTimeField(null=True)
    amount = models.DecimalField(max_digits=8,decimal_places=2)
    paid_amount = models.DecimalField(max_digits=8,decimal_places=2,default=0)
    disbursed_on = models.DateTimeField(null=True)
    is_disbursed = models.BooleanField(default=False)
    is_cleared = models.BooleanField(default=False)
    is_waived = models.BooleanField(default=False)
    is_extended = models.BooleanField(default=False)
    is_written_off = models.BooleanField(default=False)
    cleared_on = models.DateTimeField(null=True,blank=True)
    def __str__(self) -> str:
        return str(self.application.product.name + ' - '+ self.application.client.first_name +' - ' + ' #' + str(self.application.amount))

    @property
    def is_overdue(self):
        now = timezone.now()
        today = now.date()
        return today > self.date_due.date()

   
class Waiver(FactoryModel):

    loan = models.ForeignKey(Loan, on_delete=models.PROTECT)
    amount = models.DecimalField(max_digits=7,decimal_places=2)
    waived_by = models.ForeignKey('users.User',on_delete=models.DO_NOTHING)


class Extension(FactoryModel):

    loan = models.ForeignKey(Loan, on_delete=models.PROTECT)
    ext_from = models.DateTimeField()
    ext_to = models.DateTimeField()
    extended_by = models.ForeignKey('users.User',on_delete=models.DO_NOTHING)




