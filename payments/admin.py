from django.contrib import admin
from django.contrib import admin
from django.db import models
from django.utils.translation import gettext as _
from django import forms
from .models import PayOut,PayIn
# Register your models here.

class PayOutAdmin(admin.ModelAdmin):

    # fields = ('receipient_phone','amount','status','notes','created_at','application',)
    list_display = ('receipient_phone','amount','status','notes','created_at',)
    list_display_links = ('receipient_phone','amount',)
    readonly_fields = ('receipient_phone','amount','notes','created_at','loan',)

    fieldsets = (
        (None, {'fields': ('receipient_phone','amount','status','notes','created_at',)}),
        ('Loan Application Details', {'fields': ('loan',)}),
        
        
    )
    
    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False

admin.site.register(PayOut,PayOutAdmin)