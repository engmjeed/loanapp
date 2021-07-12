from flex.ussd.utils import AttributeBag
from clients.models import Client

class UserAccount(AttributeBag):
	
    balance = 0
    loan_limit = 0
    msisdn = None
    account_no = None

   