from django.contrib import admin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext as _
from django import forms
from .models import Loan,Application

# Register your models here.
class ApplicationChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    notes = forms.CharField(widget=forms.Textarea,required=False)

    class Meta:
        model =Application
        fields = ('status', 'notes',)

    

class LoanAdmin(admin.ModelAdmin):

    list_display = ('get_code','get_client','get_amount','date_due','disbursed_on',)
    list_display_links = ('get_code',)
    readonly_fields = ('get_code','get_client','get_amount',
        'date_due','disbursed_on','get_is_overdue',
        'application','is_cleared','is_waived','is_written_off',
        'cleared_on',)

    fieldsets = (
        (None, {'fields': ('get_code','get_client','get_amount','date_due','disbursed_on',)}),
        ('Loan Application Details', {'fields': ('application',)}),
        ('Other Details', {'fields': ('get_is_overdue','is_cleared','is_waived','is_written_off','cleared_on',)}),
        
    )
    def has_delete_permission(self, request, obj=None):
        return False

    def get_is_overdue(self,obj):
        now = timezone.now()
        today = now.date()
        return today > obj.date_due.date() and False
    get_is_overdue.short_description = 'Is Loan Overdue'
    
    def get_amount(self,obj):
        return obj.application.amount
    get_amount.short_description = 'Amount'

    def get_client(self,obj):
        return str(obj.application.client.first_name) + ' - ' + str(obj.application.client.msisdn)
    get_client.short_description = 'Client'

    def get_code(self,obj):
        return str(obj.application.code)
    
    get_code.short_description = '# Loan ID'
    



admin.site.register(Loan,LoanAdmin)

class LoanApplication(admin.ModelAdmin):

    form = ApplicationChangeForm
    
    list_display = ('code','client','amount','get_duration','status','created_at',)
    readonly_fields =  ('code','client','product','amount','get_duration','get_reviewed_by','created_at',)
    list_display_links = ('code',)
    fieldsets = (
        (None, {'fields': ('status','notes',)}),
        ('Client', {'fields': ('client',)}),
        ('Product', {'fields': ('product',)}),
        ('Reviews By', {'fields': ('get_reviewed_by',)}),
        
    )
    
    def has_change_permission(self, request, obj=None):
        return True

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
    
    def get_duration(self,obj):
        return obj.duration
    
    def get_reviewed_by(self,obj):
        return not obj.reviewed_by and 'System Auto'
        
    get_duration.short_description = _("Duration In Months")

    


admin.site.register(Application,LoanApplication)


 