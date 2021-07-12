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
from factory.helpers import Helpers
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

                conf = config()
                url = conf.get('payouts_url')
                r = requests.post(url,json=payload,verify=False,timeout=5)
                response = r.json()
                r_status = response.get('status')
                print(response,"response")
               
                if r_status =='created':
                    item.status = PayOutStatusEnum.PROCESSED
                    item.loan.disbursed_on = timezone.now()
                    item.loan.is_disbursed = True
                    item.notes = 'Queued'
                    item.save()
                   
                    
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




