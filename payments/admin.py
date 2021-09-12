from django.contrib import admin
from django.contrib import admin
from django.utils.translation import gettext as _
from django import forms
from .models import PayOut,PayIn
# Register your models here.

class PayOutAdmin(admin.ModelAdmin):

    # fields = ('receiving_phone','amount','status','notes','created_at','application',)
    list_display = ('receiving_phone','amount','status','notes','get_created_at',)
    list_display_links = ('receiving_phone',)
    readonly_fields = ('receiving_phone','amount','notes','created_at','loan','get_client',)

    fieldsets = (
        (None, {'fields': ('receiving_phone','amount','status','notes','get_created_at',)}),
        ('Loan Application Details', {'fields': ('loan',)}),
        ('Client Details', {'fields': ('get_client',)}), 
    )
    
    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False

    def get_client(self,obj):
        return obj.loan.application.client
    
    get_client.short_description = 'Client'

    def get_created_at(self,obj):
        return obj.created_at
    
    get_created_at.short_description = 'Initiated At'

class PayInAdmin(admin.ModelAdmin):


    list_display = ('mpesa_code','amount','get_bill_ref_no','status','transaction_date',)
    list_display_links = ('mpesa_code',)
    readonly_fields = ('client','amount','mpesa_code','get_bill_ref_no','status','notes','transaction_date',)
    search_fields = ('mpesa_code','bill_ref_no',)

    fieldsets = (
        (None, {'fields': ('mpesa_code','amount','get_bill_ref_no','status','transaction_date',)}),
        ('Being Payment for:', {'fields': ('loan',)}),
        ('Notes:', {'fields': ('notes',)}),
        
        
    )

    def get_bill_ref_no(self,instance):
        return instance.bill_ref_no
    
    get_bill_ref_no.short_description = 'Loan ID'
    

    
    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False

admin.site.register(PayIn,PayInAdmin)
admin.site.register(PayOut,PayOutAdmin)
