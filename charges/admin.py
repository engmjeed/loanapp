from django.contrib import admin
from .models import Charge

# Register your models here.

class ChargeAdmin(admin.ModelAdmin):

    list_display = ('name','description','amount','is_active',)
    # readonly_fields = ('name',)
    # ordering = ('-amount',)
    link_display = ('name',)
    fields = ('name','description','amount','is_active',)

admin.site.register(Charge,ChargeAdmin)


 