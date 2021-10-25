from flex.ussd.utils.decorators import lookup_property
from logging import fatal
from django.contrib import admin
from django import forms
from django.db import models
from .models import Client,LoanProfile
from django.forms import formset_factory
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from transactions.models import Transaction
from factory.helpers import helpers
from django_reverse_admin import ReverseModelAdmin

# Register your models here.
class ClientResource(resources.ModelResource):

    class Meta:
        model = Client

class TransactionForm(forms.ModelForm):

    model = Client
    
    def __init__(self, *args, **kwargs):
            super(TransactionForm, self).__init__(*args, **kwargs)
            if self.instance:
                # fill initial related values
                self.fields['transactions'].initial = self.instance.transactions.all()

        
class ClientChangeForm(forms.ModelForm):
    model = Client
    resource_class = ClientResource

    fields = ('msisdn','first_name','last_name','id_no','pin','center','is_active',)
class LoanProfileInline(admin.TabularInline):

    model = LoanProfile
    
    fk_name = 'client'
    fields = ('product','minimum_principle','maximum_principle','loan_limit','available_limit','is_active',)
    # readonly_fields = ('product','minimum_principle','maximum_principle','loan_limit','available_limit','is_active',)
    
    def has_change_permission(self, request, obj=None):
        if not obj:
            return True
        else:
            return False

    def has_add_permission(self, request, obj=None):
        return True

    def has_delete_permission(self, request, obj=None):
        return False

    extra = 0

    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):

        field = super(LoanProfileInline,self).formfield_for_foreignkey(db_field, request, **kwargs)

        if db_field.name == 'client':
            if request._obj_ is not None:
                field.queryset = field.queryset.filter(product__exact=request._obj_)
            else:
                field.queryset = field.queryset.none()
        return field


class ClientTransactionInline(admin.TabularInline):

    model = Transaction
    # formset =  MyFormSet
    
    fk_name = 'client'
    list_display = ('product','type','subject','initial_balance','amount','final_balance')
    fields = ('product','type','subject','initial_balance','amount','final_balance',)
    readonly_fields = ('product','type','subject','initial_balance','amount','final_balance',)
    list_filter = ('product','type',)
    
    def has_change_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    extra = 0
    
    def get_queryset(self, request):
        return super().get_queryset(request).order_by('created_at')
        


    
class ClientAdmin(admin.ModelAdmin):

    # resource_class = ClientResource

    inlines = (
        LoanProfileInline,
        ClientTransactionInline
    )
    
        
    # inlineformset_factory = LoanProfileFormSet
    list_display = ('msisdn','first_name','last_name','id_no','pin','center','is_active',)
    # readonly_fields = ('msisdn','first_name','last_name','id_no','pin','center',)
    # ordering = ('-amount',)
    link_display = ('msisdn',)
    list_filter = ('is_active',)
    lookup_property = ('msisdn','first_name',)
    search_fields = ('msisdn','first_name','last_name','id_no','pin','center',)
    # fields = ('msisdn','first_name','last_name','id_no','pin','center','is_active','products','officer',)
    fieldsets = (
        (None, {'fields': ('msisdn','first_name','last_name','id_no','pin','center','is_active',)}),
        ('Listed Products', {'fields': ('products',)}),
        ('Loan Officer', {'fields': ('officer',)}),

        
    )
    def get_formsets_with_inlines(self, request, obj=None):
        for inline in self.get_inline_instances(request, obj):
            # hide LoanProfileInline in the add view
            if not isinstance(inline, LoanProfileInline) or obj is not None:
                yield inline.get_formset(request, obj), inline
    
    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super().get_inline_instances(request, obj)
    
    def has_delete_permission(self, request, obj=None):
        return False
    filter_vertical = ()

    


admin.site.register(Client,ClientAdmin)




