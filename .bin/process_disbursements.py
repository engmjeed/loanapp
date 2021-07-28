from django import conf
from django.utils import timezone
from env import Env
import requests
from payments.models import PayOut,PayOutStatusEnum
import time
import urllib3
import json
from django.conf import settings
import hashlib
import logging
from dateutil.relativedelta import relativedelta
from factory.helpers import Helpers
from transactions.models import TransactionTypeEnum
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

logger = logging.getLogger(__name__)
helpers = Helpers()


def config():
    return settings.IPN_CONFIG

def get_key(msisdn,amount,reference_number,short_code):
    conf = config()
    app_key = conf.get('app-key')
    app_secret = conf.get('app-secret')
    

    key_text=(msisdn+str(amount)+app_key+app_secret+reference_number+short_code).encode('utf-8')
    return hashlib.sha256(key_text).hexdigest()


def run():
    ROWS_SELECTION_LIMIT=50
    conf = config()



    while True:
        payouts = PayOut.get_unprocessed(limit=ROWS_SELECTION_LIMIT)

        for item in payouts:
            try:
                loan_profile = helpers.get_client_product_loan_profile(
                    item.loan.application.client,
                    item.loan.application.product
                    )
                msisdn = item.receipient_phone
                amount = int(item.amount)
                ref_no = item.loan.application.ref_no
                short_code = conf.get('short_code')
                key = get_key(msisdn,amount,ref_no,short_code)

                payload = { 'msisdn':msisdn,
                            'amount':amount,
                            'ref_no':ref_no,
                            'short_code':short_code,
                            'key':key
                          }
                url = conf.get('payouts_url')
                r = requests.post(url,json=payload,verify=False,timeout=20)
                response = r.json()
                r_status = response.get('status')
                print(response,"response")
               
                if r_status =='created':
                    date_due = timezone.now() + relativedelta(months=item.loan.application.duration)
                    item.status = PayOutStatusEnum.PROCESSED
                    item.loan.disbursed_on = timezone.now()
                    item.loan.is_disbursed = True
                    item.notes = 'Queued'
                    item.loan.date_due = date_due
                    item.save()
                    loan_profile.available_limit -= item.loan.application.amount
                    loan_profile.save()
                    helpers.create_transaction(
                    client=item.loan.application.client,
                    type = TransactionTypeEnum.DEBIT,
                    product=item.loan.application.product,
                    subject='Loan Disbursement',
                    initial_balance = loan_profile.available_limit,
                    amount = item.loan.application.amount,
                    ref=item.loan)
                   
                    
                else:
                    item.status = PayOutStatusEnum.ERRORED
                    item.notes = response.get('status')
                    item.save()
                    logger.error(f"{response.get('status')}")


            except requests.exceptions.Timeout as exc:
                item.notes= "Disbursement Timed Out"
                item.status = PayOutStatusEnum.ERRORED
                item.save()
                logger.error(f'{repr(exc)}')

            except requests.exceptions.ConnectionError  as exc:
                item.notes= "Disbursement Timed Out"
                item.status = PayOutStatusEnum.ERRORED
                item.save()
                logger.error(f'{repr(exc)}')

            except json.JSONDecodeError as exc:
                item.notes = "Error on Disbursement"
                item.status = PayOutStatusEnum.ERRORED
                item.save()
                logger.error(f'{repr(exc)}')

            except Exception as exc:
                item.notes = "Error on Disbursement"
                item.status = PayOutStatusEnum.ERRORED
                item.save()
                logger.error(f'{repr(exc)}')





        time.sleep(10) #wait  seconds before processing again



#runs
run()




