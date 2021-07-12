from datetime import datetime
import requests
import time
import json

from env import Env #import even when not using.

from django.conf import settings
from django.utils import timezone
from django.db import transaction
from loans.models import Application,ApplicationStatusEnum,Loan
from payments.models import PayOut
from dateutil.relativedelta import relativedelta
from django.utils import timezone
from factory.helpers import helpers

 


def run():
    
    ROWS_SELECTION_LIMIT=50
    




    while True:
        #get un processed applications for processing

        applications=Application.get_unprocessed(limit=ROWS_SELECTION_LIMIT)
        for application in applications:

            

            try:
                loan_profile = helpers.get_client_product_loan_profile(application.client,application.product)
                
                if loan_profile.available_limit < application.amount:
                    application.status = ApplicationStatusEnum.REJECTED
                    application.notes = 'Loan Amount more than Available Loan Limit'
                    application.save()
                    continue
                elif not application.client.is_active:
                    application.status = ApplicationStatusEnum.REJECTED
                    application.notes = 'Client is in Inactive State'
                    application.save()
                    continue
                else:

                    date_due = timezone.now() + relativedelta(months=application.duration)
                    disbursed_on = timezone.now()
                    with transaction.atomic():
                        loan = Loan.objects.create(application=application,date_due=date_due)
                        payout = PayOut.create(loan=loan)
                    application.status = ApplicationStatusEnum.PROCESSED
                    application.notes = 'Loan Application Queued for Processing'
                    application.save()
                    loan_profile.available_limit -= application.amount
                    loan_profile.save()
                    print("Successfully Added payout")


                
                
            

            except Exception as exc:
                print(f'{repr(exc)}')
                application.status = ApplicationStatusEnum.FAILED
                application.notes = 'Application Processing Failed'
                application.save()


        time.sleep(1) #wait  seconds before processing again



#runs
run()




