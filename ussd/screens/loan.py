from collections import OrderedDict
from datetime import timedelta
from django.utils import timezone

from django.utils.timezone import is_aware
from products.models import Product
from clients.models import LoanProfile

from flex.ussd.screens import UssdScreen, render_screen
from dateutil.relativedelta import relativedelta
from .mixins import ScreenMixin
from django.conf import settings
from .utils import fetcher
from factory.helpers import helpers


class LoanProductsScreen(UssdScreen, ScreenMixin):
	


	class Meta:
		label = 'products'


	def handle_input(self, *args):
		if len(args) > 1 or args[0] not in self.state.menu:
			self.error(self.ERRORS.INVALID_CHOICE)
			return self.render_menu()

		opt = self.state.menu[args[0]]
		product = Product.objects.get(pk=opt[1])
		
		return render_screen('jl.loan_amount',product=product)
	
	def render_menu(self):
		self.get_menu()
		self.print('Choose Product')
		for k, v in self.state.menu.items():
			self.print(str(k) + ':',v[0])
		return self.CON
		
	def get_menu(self):
		menu = fetcher.fetch_products_menu(
			self.session.client.products.filter(
				is_active=True
				).order_by(
					'id'
				).values_list(
						'name',
						'id',
			
				)
			)
		self.state.menu = menu
		
	def render(self, opt=None, *args):
		if opt is not None and not args:
			return self.handle_input(opt)
		if args:
			self.print('Invalid choice.')
		return self.render_menu()


class LoanAmountScreen(UssdScreen, ScreenMixin):

	
	class Meta:
		label = 'loan_amount'


	def handle_input(self, opt):
		amount = int(opt)
		loan_profile = self.get_client_product_loan_profile()
		limit = loan_profile.loan_limit
		if amount > limit:
			self.print(f'{amount} KES is greater than your Loan limit for this product')
			self.print(f'Enter an amount less than {limit} KES')
			return self.CON
		elif amount < loan_profile.minimum_principle:
			self.print(f'Minimum Loan allowed for {loan_profile.product.name} Product is {loan_profile.minimum_principle} KES')
			self.print(f'Enter amount greater than {loan_profile.minimum_principle} KES')
			return self.CON

		else:
			return render_screen('jl.loan_period',product=self.state.product,loan_profile=loan_profile,amount=amount)
	
	def render_menu(self):
		self.print('Enter Amount')
		return self.CON
	
	def render(self, opt=None, *args):
		if opt is not None and not args:
			return self.handle_input(opt)
		if args:
			self.print('Invalid choice.')
		return self.render_menu()

	def get_client_product_loan_profile(self):
		product = self.state.product
		return LoanProfile.objects.get(product=product,client=self.session.client)


class LoanPeriodScreen(UssdScreen, ScreenMixin):

	
	class Meta:
		label = 'loan_period'


	def handle_input(self, opt):
		try:
			period = int(opt)
			return render_screen('jl.loan_confirmation',
				period=period,
				product=self.state.product,
				loan_profile=self.state.loan_profile,
				amount = self.state.amount)
		except:
			self.print('Enter a valid Loan Period')
			return self.CON
	
	def render_menu(self):
		self.get_menu()
		self.print('Enter Loan Duration')
		for k, v in self.state.menu.items():
			self.print(str(k) + ':',v)
		return self.CON
	
	
	def render(self, opt=None, *args):
		if opt is not None and not args:
			return self.handle_input(opt)
		if args:
			self.print('Invalid choice.')
		return self.render_menu()

	def get_menu(self):
		menu = fetcher.make_loan_duration_menu(self.state.product.max_repayment_months+1)
		self.state.menu = menu

class LoanCornifirmationScreen(UssdScreen, ScreenMixin):

	MENU_ITEMS = OrderedDict([
	('1', ("Proceed", "jl.loan_complete")),
	('2', ("Cancel", "jl.loan_cancel")),
	
])

	
	class Meta:
		label = 'loan_confirmation'


	def handle_input(self, *args):
		if len(args) > 1 or args[0] not in self.MENU_ITEMS:
			self.error(self.ERRORS.INVALID_CHOICE)
			return self.render_menu()

		opt = self.MENU_ITEMS[args[0]]
	
		return render_screen(opt[1],product= self.state.product,amount= self.state.amount,period=self.state.period)
	
	def render_menu(self):
		charges = 0
		for charge in self.state.product.charges.all():
			charges+= charge.amount
		interest = self.calculate_interest()
		due_date = timezone.now() + relativedelta(months=self.state.period)
		self.print(f'Borrow {self.state.amount} for {self.state.period} Month(s)')
		self.print(f'Charges {charges}')
		self.print(f'Interest {interest}')
		self.print(f'Due On {self.format_date(due_date)}')
		self.print(f'Total Loan {self.state.amount + charges+interest}')
		for k, v in self.MENU_ITEMS.items():
			self.print(str(k) + ':',v[0])
		return self.CON
	
	
	def render(self, opt=None, *args):
		if opt is not None and not args:
			return self.handle_input(opt)
		if args:
			self.print('Invalid choice.')
		return self.render_menu()

	def calculate_interest(self):
		interest = (self.state.amount*self.state.product.interest_rate*self.state.period)//100
		return interest


class LoanProductInfoScreen(UssdScreen, ScreenMixin):

	MENU_ITEMS = OrderedDict([
	('1', ("Proceed", "jl.not_implemented")),
	('2', ("Cancel", "jl.not_implemented")),
	
])

	class Meta:
		label = 'product_info'


	def handle_input(self, *args):
		pass
	
	def render_menu(self):
		product = self.state.product
		# self.print(f'Name: {product.name}')
		self.print(f'Interest Rate(PM): {product.interest_rate}%')
		self.print('Charges:')
		for charge in product.charges.filter(is_active=True):
			self.print(f'{charge.name} - {charge.amount} (KES) ')
		
		for k, v in self.MENU_ITEMS.items():
			self.print(str(k) + ':',v[0])
		return self.CON
	
	def render(self, opt=None, *args):
		if opt is not None and not args:
			return self.handle_input(opt)
		if args:
			self.print('Invalid choice.')
		return self.render_menu()

class LoanCompleteScreen(UssdScreen, ScreenMixin):
	nav_menu = None

	class Meta:
		label = 'loan_complete'



	def handle_input(self, *args):
		pass

	def render_menu(self):
		helpers.create_loan_application(self.session.client,self.state.product,self.state.amount,self.state.period)
		self.print('Your Loan is being Processed.Thank you.')
		
		return self.END

	def get_menu(self):
		pass
		
	def render(self, opt=None, *args):
		if opt is not None and not args:
			return self.handle_input(opt)
		if args:
			self.print('Invalid choice.')
		return self.render_menu()

class LoanCancelScreen(UssdScreen, ScreenMixin):
	nav_menu = None

	class Meta:
		label = 'loan_cancel'



	def handle_input(self, *args):
		pass

	def render_menu(self):
		self.print('Your Request has been cancelled. Hope to see you soon.')
		
		return self.END

	def get_menu(self):
		pass
		
	def render(self, opt=None, *args):
		if opt is not None and not args:
			return self.handle_input(opt)
		if args:
			self.print('Invalid choice.')
		return self.render_menu()
