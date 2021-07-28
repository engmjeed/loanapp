from django import conf
from django.utils import timezone
from env import Env
from django.db import models, transaction
from transactions.models import TransactionTypeEnum
from payments.models import PayIn,PayInStatusEnum
import time
import json
from django.conf import settings
import logging
from factory.helpers import Helpers


logger = logging.getLogger(__name__)
helpers = Helpers()

def run():
    ROWS_SELECTION_LIMIT=50




    while True:
        payins = PayIn.get_unprocessed(limit=ROWS_SELECTION_LIMIT)

        for item in payins:
            loan_profile = helpers.get_client_product_loan_profile(
                    item.client,
                    item.loan.application.product
                    )
            loan = item.loan
            amount = item.amount
            loan_amount = item.loan.amount
            try:
                with transaction.atomic():
                    loan_profile.available_limit+=amount
                    loan_profile.save()
                    if loan_amount <= amount:
                        loan.is_cleared = True
                        loan.cleared_on = timezone.now()
                    loan.paid_amount = amount
                    loan.save()
                    item.status = PayInStatusEnum.PROCESSED
                    
                    helpers.create_transaction(
                    client=item.loan.application.client,
                    type = TransactionTypeEnum.CREDIT,
                    product=item.loan.application.product,
                    subject='Loan Repayment',
                    initial_balance = loan_amount,
                    amount = amount,
                    ref=item.loan)
                    item.save()
                    print('Processed')

            except Exception as exc:
                item.notes = "Error Processing Payin"
                item.status = PayInStatusEnum.ERRORED
                item.save()
                print('ERROR')
                logger.error(f'{repr(exc)}')





        time.sleep(5) #wait  seconds before processing again



#runs
run()




