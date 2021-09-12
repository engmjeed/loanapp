from django import conf
from django.utils import timezone
from env import Env
import requests
from payments.models import Checkout, CheckOutStatusEnum
import time
import urllib3
import json
from django.conf import settings
import hashlib
import logging
from factory.helpers import Helpers
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

logger = logging.getLogger(__name__)
from factory.helpers import helpers


def config():
    return settings.VARIABLES
def run():
    ROWS_SELECTION_LIMIT=50
    



    while True:
        checkouts = Checkout.get_unprocessed(limit=ROWS_SELECTION_LIMIT)

        for item in checkouts:
            try:
                headers={"Authorization":"Bearer %s" % helpers.generate_token()}
                payload = {
					"BusinessShortCode": settings.VARIABLES.get('BUSINESS_SHORTCODE'),
					"Password": settings.VARIABLES.get('PASSWORD'),
					"Timestamp": settings.VARIABLES.get('Timestamp'),
					"TransactionType": "CustomerPayBillOnline",
					"Amount": item.amount,
					"PartyA": item.msisdn,
					"PartyB": settings.VARIABLES.get('BUSINESS_SHORTCODE'),
					"PhoneNumber": item.msisdn,
					"CallBackURL": settings.VARIABLES.get('DEFAULTCALLBACKURL'),
					"AccountReference":item.ref_no,
					"TransactionDesc": 'Jijenge Loans'
			    }
                
               
                response=requests.post(settings.VARIABLES.get('PAY_URL'),json=payload,headers=headers,verify=False,timeout=30)
                print(response.text)
                rv = response.json()
                if response.status_code == requests.codes.ok:
                    item.status = CheckOutStatusEnum.PROCESSED
                    item.notes = 'Processed'
                    item.save()     
                else:
                    item.status = CheckOutStatusEnum.ERRORED
                    item.notes = 'Errored'
                    item.save() 


            except requests.exceptions.Timeout as exc:
                item.notes= "Checkout Timed Out"
                item.status = CheckOutStatusEnum.ERRORED
                item.save()
                logger.error(f'{repr(exc)}')

            except requests.exceptions.ConnectionError  as exc:
                item.notes= "Checkout Timed Out"
                item.status = CheckOutStatusEnum.ERRORED
                item.save()
                logger.error(f'{repr(exc)}')

            except json.JSONDecodeError as exc:
                item.notes = "Error on Checkout"
                item.status = CheckOutStatusEnum.ERRORED
                item.save()
                logger.error(f'{repr(exc)}')

            except Exception as exc:
                item.notes = "Error on Checkout"
                item.status = CheckOutStatusEnum.ERRORED
                item.save()
                logger.error(f'{repr(exc)}')





        time.sleep(1) #wait  seconds before processing again



#runs
run()




