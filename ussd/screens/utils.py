from collections import OrderedDict
from loans.models import Loan


class Fetcher:

	def fetch_products_menu(self,products):
		ls = []
		ls.extend(((str(i), x) for i,x in enumerate(products, 1)))
		ls = OrderedDict(ls)
		
		return ls


	def make_menu(self,obj):
		ls = []
		ls.extend(((str(i), x) for i,x in enumerate(obj, 1)))
		ls = OrderedDict(ls)
		return ls

	def make_loan_duration_menu(self,max_repayment_months):
		ls = []
		ls.extend(((str(i), str(x) +' Month(s)') for i,x in enumerate(range(1,max_repayment_months), 1)))
		ls = OrderedDict(ls)
		return ls
	def get_my_loans_menu(self,client):
		ls = []
		menu = Loan.objects.filter(is_disbursed=True,application__client=client).order_by('-id').values_list('application__product__name','pk','amount')
		ls.extend(((str(i), x) for i,x in enumerate(menu, 1)))
		ls = OrderedDict(ls)
		return ls


fetcher = Fetcher()



	

