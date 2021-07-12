from django.db import models
from django.db.models import constraints
from phonenumber_field.modelfields import PhoneNumberField
from factory.models import FactoryModel
from django.conf import settings
# Create your models here.

class Client(FactoryModel):
    
    msisdn = PhoneNumberField(db_index=True)
    first_name = models.CharField(max_length=15)
    middle_name = models.CharField(max_length=15,null=True,blank=True)
    last_name = models.CharField(max_length=15)
    id_no = models.BigIntegerField()
    pin = models.CharField(max_length=20,null=True,blank=True)
    is_active = models.BooleanField(default=False)
    products = models.ManyToManyField('products.Product',related_name='products')
    officer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING)
    center = models.ForeignKey('organisations.Center', on_delete=models.DO_NOTHING)

    def __str__(self) -> str:
        return self.first_name + '-: ' + str(self.msisdn)

    class Meta:
        constraints = [
                
                models.UniqueConstraint(name="%(app_label)s_%(class)s_unique_center_client",
                    fields=['center','msisdn'],
                    )
            ]

class LoanProfile(FactoryModel):
    
    id = models.BigIntegerField(primary_key=True)
    minimum_principle = models.DecimalField(max_digits=7,decimal_places=2,null=True,blank=True)
    maximum_principle = models.DecimalField(max_digits=7,decimal_places=2,null=True,blank=True)
    loan_limit = models.DecimalField(max_digits=8,decimal_places=2,default=0)
    available_limit = models.DecimalField(max_digits=8,decimal_places=2,default=0)
    auto_approve = models.BooleanField(default=True)
    auto_approve_ceiling = models.DecimalField(max_digits=7,decimal_places=2,default=settings.AUTO_APPROVE_CEILING)
    product = models.ForeignKey('products.Product', on_delete=models.PROTECT)
    client = models.ForeignKey(Client, on_delete=models.PROTECT,related_name='loan_profile')
    is_active = models.BooleanField(default=False)

    def __str__(self) -> str:
        return '#'+ str(self.id)

    class Meta:
        constraints = [
                
                models.UniqueConstraint(name="%(app_label)s_%(class)s_unique_product_client",
                    fields=['product','client'],
                    )
            ]
