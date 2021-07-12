from django.db import models
from factory.models import FactoryModel
from django_extensions.db.fields import AutoSlugField

# Create your models here.
class Product(FactoryModel):

    name = models.CharField(max_length=30)
    slug = AutoSlugField(populate_from=('name',),unique=True, max_length=255, overwrite=True)
    short_name = models.CharField(max_length=10)
    description = models.CharField(max_length=255, null=True)
    minimum_principal = models.DecimalField(max_digits=7,decimal_places=2)
    maximum_principal = models.DecimalField(max_digits=8,decimal_places=2)
    is_active = models.BooleanField(default=True)
    interest_rate = models.DecimalField(max_digits=4,decimal_places=2)
    max_repayment_months = models.IntegerField()
    charges = models.ManyToManyField('charges.Charge',related_name='charges')
    fund = models.ForeignKey('funds.Fund', on_delete= models.PROTECT)
    
    def __str__(self):
        return self.slug or self.name
