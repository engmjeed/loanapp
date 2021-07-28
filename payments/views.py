from django.shortcuts import render
from django.views import View
from factory.helpers import helpers
from payments.models import PayIn
from django.http import HttpResponse,JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import arrow
import json

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

