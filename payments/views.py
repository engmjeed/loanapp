from email.mime import application
from django.shortcuts import render
from django.views import View
from factory.helpers import helpers
from payments.models import PayIn, PayOutStatusEnum
from payments.models import PayOut,PayInStatusEnum
from loans.models import Application,ApplicationStatusEnum,Loan
from django.http import HttpResponse,JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.utils import timezone
import arrow
import json
from django.shortcuts import get_object_or_404

# Create your views here.

class Payins(View):
    
    def post(self,request):
        data = json.loads(request.body.decode('utf-8'))
        transaction_id = data.get('TransID')
        transaction_time = data.get('TransTime')
        transaction_amount = data.get('TransAmount')
        bill_reference_number = data.get('BillRefNumber')
        msisdn = data.get('MSISDN')
        
        
        client = helpers.get_client_by_msisdn(msisdn)
        loan = helpers.get_loan_by_code(bill_reference_number)
        timestamp = arrow.get(transaction_time, "YYYYMMDDHHmmss")
        transaction_date = timestamp.datetime
        PayIn.objects.create(
            client=client,
            loan = loan,
            amount=transaction_amount,
            mpesa_code=transaction_id,
            bill_ref_no=bill_reference_number,
            transaction_date=transaction_date,
            
            raw = data,
            )
    
        return JsonResponse({'status':'Accepted'})

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

class PayoutResponse(View):
    def post(self,request):
        data = json.loads(request.body.decode('utf-8'))

        ref_no = data.get('transaction_id')
        result_code = data.get('result_code')
        results = data.get('results')
        notes = data.get('result_description')
        mpesa_code = data.get('mpesa_transaction_id')
        l_application = get_object_or_404(Application,ref_no=ref_no)
        loan = get_object_or_404(Loan, application=l_application)
        payout = get_object_or_404(PayOut,loan=loan)
        payout.notes = notes
        payout.result_code = result_code
        payout.results=results
        payout.mpesa_code = mpesa_code
        payout.status = PayOutStatusEnum.PROCESSED
        payout.save()
        loan.is_disbursed = True
        loan.disbursed_on = timezone.now()
        loan.save()
        l_application.status = ApplicationStatusEnum.PROCESSED
        l_application.save()
        return JsonResponse({'status':'Accepted'})

    def get(self,request):
        return JsonResponse({'status':'Method Not Allowed'},status=405)


    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    







