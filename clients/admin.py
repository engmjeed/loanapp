from logging import fatal
from django.contrib import admin
from django import forms
from django.db import models
from .models import Client,LoanProfile
from django.forms import formset_factory
from import_export import resources
from import_export.admin import ImportExportModelAdmin




# Register your models here.
class ClientResource(resources.ModelResource):

    class Meta:
        model = Client
        
class ClientChangeForm(forms.ModelForm):
    model = Client
    fields = ('msisdn','first_name','last_name','id_no','pin','center','is_active',)
class LoanProfileInline(admin.TabularInline):

    model = LoanProfile
    
    fk_name = 'client'
    fields = ('product','minimum_principle','maximum_principle','loan_limit','available_limit','is_active',)
    readonly_fields = ('product','minimum_principle','maximum_principle','loan_limit','available_limit','is_active',)
    
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

        field = super(LoanProfileInline, self).formfield_for_foreignkey(db_field, request, **kwargs)

        if db_field.name == 'client':
            if request._obj_ is not None:
                field.queryset = field.queryset.filter(product__exact=request._obj_)
            else:
                field.queryset = field.queryset.none()

        return field

class ClientAdmin(ImportExportModelAdmin,admin.ModelAdmin):

    resource_class = ClientResource


    inlines = (
        LoanProfileInline,
    )
    
        
    # inlineformset_factory = LoanProfileFormSet
    list_display = ('msisdn','first_name','last_name','id_no','pin','center','is_active',)
    # readonly_fields = ('msisdn','first_name','last_name','id_no','pin','center',)
    # ordering = ('-amount',)
    link_display = ('name',)
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
        return super(ClientAdmin, self).get_inline_instances(request, obj)
    
    def has_delete_permission(self, request, obj=None):
        return False
    


admin.site.register(Client,ClientAdmin)



