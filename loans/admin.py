from django.contrib import admin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext as _
from django import forms
from .models import Loan,Application,ApplicationStatusEnum
from factory.helpers import helpers
from django.contrib.contenttypes.models import ContentType
from django.core.paginator import Paginator
from django.utils.html import format_html_join
from django.utils.safestring import mark_safe
from transactions.models import TransactionTypeEnum



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

    list_display = ('get_code','get_client','get_amount','get_charges','get_total_amount','date_due',)
    list_display_links = ('get_code',)
    readonly_fields = ('get_code','get_client','get_amount','get_charge_details',
        'get_charges','get_total_amount',
        'date_due','disbursed_on','get_is_overdue',
        'application','is_cleared','is_waived','is_written_off',
        'cleared_on','get_is_disbursed','get_loan_balance','paid_amount',)
    # list_per_page = 3
    # paginator = Paginator

    fieldsets = (
        (None, {'fields': ('get_code','get_client','get_amount','get_charges','get_total_amount','date_due',)}),
        ('Loan Application Details', {'fields': ('application',)}),
        ('Disbursement Status', {'fields': ('get_is_disbursed','disbursed_on',)}),
        ('Charges Detail', {'fields': ('get_charge_details',)}),
        ('Repayments Info', {'fields': ('paid_amount','get_loan_balance',)}),
        ('Other Details', {'fields': ('get_is_overdue','is_cleared','is_waived','is_written_off','cleared_on',)}),
        
    )
    def has_delete_permission(self, request, obj=None):
        return False
    def has_add_permission(self, request, obj=None):
        return False

    def get_is_overdue(self,obj):
        now = timezone.now()
        today = now.date()
        return today > obj.date_due.date() and False
    get_is_overdue.short_description = 'Is Loan Overdue'
    
    def get_amount(self,obj):
        return obj.application.amount
    get_amount.short_description = 'Requested Amount'

    def get_charges(self,obj):
        charges = 0
        for charge in obj.application.product.charges.all():
            charges+=charge.amount
        loan_interest = helpers.calculate_interest(obj.application)
        charges+=loan_interest
        return charges
    get_charges.short_description = 'Total Charges'

    def get_total_amount(self,obj):
        return obj.amount
    get_total_amount.short_description = 'Total Loan Amount'

    def get_client(self,obj):
        return str(obj.application.client.first_name) + ' - ' + str(obj.application.client.msisdn)
    get_client.short_description = 'Client'

    def get_code(self,obj):
        return str(obj.application.code)
    
    get_code.short_description = '# Loan ID'

    def get_charge_details(self,obj):
        details = []
        for charge in obj.application.product.charges.all():
            details.append(f'{charge.name} - {charge.amount}')
        return details
    
    get_charge_details.short_description = 'Detail'

    def get_is_disbursed(self,obj):
        return 'Disbursed' if obj.is_disbursed else 'Not Disbursed'

    get_is_disbursed.short_description = 'Disbursement Status'

    def get_loan_balance(self,obj):
        return obj.amount - obj.paid_amount

    get_loan_balance.short_description = 'Loan Balance'

   
    def get_repayments(self,obj):
        
        return format_html_join(
            mark_safe('<br>'),
            '{}',
            ((line,) for line in self.get_transactions(obj)),
        ) or mark_safe("<span class='errors'>I can't determine this address.</span>")

    get_repayments.short_description = 'Repayments Info'
    
    def get_transactions(self,obj):
        transactions_list = []
        print("we are here")
        transaction_type = ContentType.objects.get(app_label='loans', model='loan')
        print('Transaction tyoe',transaction_type)
        transactions = transaction_type.get_object_for_this_type(
            pk=obj.pk
            )
        transactions_list.append(transactions.amount)
        transactions_list.append(transactions.paid_amount)

        print('List',transactions_list)
        return transactions_list

        

    
    



admin.site.register(Loan,LoanAdmin)

class LoanApplication(admin.ModelAdmin):

    form = ApplicationChangeForm
    
    list_display = ('code','client','amount','get_duration','status','created_at',)
    readonly_fields =  ('code','client','product','amount','get_duration','get_reviewed_by','created_at',)
    list_display_links = ('code',)
    list_filter = ('status',)
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

    # def get_queryset(self, request):
    #     return super().get_queryset(request).filter(status=ApplicationStatusEnum.PENDING)

    


admin.site.register(Application,LoanApplication)


 