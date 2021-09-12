from django.contrib import admin
from .models import Product

# Register your models here.

class ProductAdmin(admin.ModelAdmin):

    list_display = ('name','short_name','minimum_principal','maximum_principal','interest_rate','max_repayment_months','fund','is_active',)
    # readonly_fields = ('name',)
    link_display = ('name',)
    # fields = ('name','short_name','minimum_principal','maximum_principal','interest_rate','max_repayment_months','fund','is_active',)

    list_filter = ('is_active',)
    preserve_filters = False
    
    fieldsets = (
        (None, {'fields': ('name','short_name','minimum_principal','maximum_principal','interest_rate','max_repayment_months',)}),
        ('Applied Charges', {'fields': ('charges',)}),
        ('Linked Fund', {'fields': ('fund',)}),
    
    )

    def has_delete_permission(self, request, obj=None):
        return False

admin.site.register(Product,ProductAdmin)

