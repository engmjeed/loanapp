from collections import OrderedDict
from loans.models import Loan
from django.utils.timezone import is_aware
from flex.ussd.screens import UssdScreen, render_screen
from .mixins import ScreenMixin
from django.conf import settings
from products.models import Product
from clients.models import LoanProfile
from .utils import fetcher
from factory.helpers import helpers

class MyAccountHomeScreen(UssdScreen, ScreenMixin):
	
	MENU_ITEMS = OrderedDict([
	('1', ("Available Balance", "jl.loan_balance_home")),
	('2', ("My Limit", "jl.loan_limit_home")),
	('3', ("My Loans", "jl.my_loans")),
	
	
])

	class Meta:
		label = 'my_account_home'


	def handle_input(self, *args):
		if len(args) > 1 or args[0] not in self.MENU_ITEMS:
			self.error(self.ERRORS.INVALID_CHOICE)
			return self.render_menu()

		opt = self.MENU_ITEMS[args[0]]
		
		return render_screen(opt[1])

	def render_menu(self):
		for k, v in self.MENU_ITEMS.items():
			self.print(str(k) + ':',v[0])
		return self.CON
		
	def get_menu(self):
		pass
		
	def render(self, opt=None, *args):
		if opt is not None and not args:
			return self.handle_input(opt)
		if args:
			self.print('Invalid choice.')
		return self.render_menu()


class LoanBalanceHomeScreen(UssdScreen, ScreenMixin):
	


	class Meta:
		label = 'loan_balance_home'


	def handle_input(self, *args):
		if len(args) > 1 or args[0] not in self.state.menu:
			self.error(self.ERRORS.INVALID_CHOICE)
			return self.render_menu()

		opt = self.state.menu[args[0]]
		product = Product.objects.get(pk=opt[1])
		
		return render_screen('jl.loan_balance',product=product)
	
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

class LoanLimitHomeScreen(UssdScreen, ScreenMixin):
	


	class Meta:
		label = 'loan_limit_home'


	def handle_input(self, *args):
		if len(args) > 1 or args[0] not in self.state.menu:
			self.error(self.ERRORS.INVALID_CHOICE)
			return self.render_menu()

		opt = self.state.menu[args[0]]
		product = Product.objects.get(pk=opt[1])
		
		return render_screen('jl.loan_limit',product=product)
	
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


class LoanBalanceScreen(UssdScreen, ScreenMixin):
	nav_menu = None

	class Meta:
		label = 'loan_balance'



	def handle_input(self, *args):
		pass

	def render_menu(self):
		loan_profile = self.get_client_product_loan_profile()

		
		self.print(f"Your Available Balance for {self.state.product.name} is {loan_profile.available_limit}")
		
		return self.END

	def render(self, opt=None, *args):
		if opt is not None and not args:
			return self.handle_input(opt)
		if args:
			self.print('Invalid choice.')
		return self.render_menu()
	def get_client_product_loan_profile(self):
		product = self.state.product
		return LoanProfile.objects.get(product=product,client=self.session.client)

class LoanLimitScreen(UssdScreen, ScreenMixin):
	nav_menu = None

	class Meta:
		label = 'loan_limit'



	def handle_input(self, *args):
		pass

	def render_menu(self):
		loan_profile = self.get_client_product_loan_profile()

		
		self.print(f"Your Loan Limit for {self.state.product.name} is {loan_profile.loan_limit}")
		
		return self.END

	def render(self, opt=None, *args):
		if opt is not None and not args:
			return self.handle_input(opt)
		if args:
			self.print('Invalid choice.')
		return self.render_menu()
	def get_client_product_loan_profile(self):
		product = self.state.product
		return LoanProfile.objects.get(product=product,client=self.session.client)

class MyLoansScreen(UssdScreen, ScreenMixin):
	nav_menu = None

	class Meta:
		label = 'my_loans'



	def handle_input(self, *args):
		if len(args) > 1 or args[0] not in self.state.menu:
			self.error(self.ERRORS.INVALID_CHOICE)
			return self.render_menu()

		opt = self.state.menu[args[0]]
		loan = Loan.objects.get(pk=opt[1])
		return render_screen('jl.loan_details',loan=loan)

	def render_menu(self):
		self.get_menu()
		if len(self.state.menu) > 0:
			self.print('Select to View and Pay ')
			for k, v in self.state.menu.items():
				self.print(str(k) + ':',v[0] + '- KES ' + str(v[2]))
			return self.CON
		else:
			self.print('You currently do not have any Loan')
			return self.END

	def render(self, opt=None, *args):
		if opt is not None and not args:
			return self.handle_input(opt)
		if args:
			self.print('Invalid choice.')
		return self.render_menu()
	def get_menu(self):
		menu = fetcher.get_my_loans_menu(self.session.client)
		self.state.menu = menu
		

class LoansDetailsScreen(UssdScreen, ScreenMixin):
	
	MENU_ITEMS = OrderedDict([
	('1', ("Pay whole Amount", "jl.pay")),
	('2', ("Pay Partially", "jl.pay_part")),
	
])

	class Meta:
		label = 'loan_details'



	def handle_input(self, *args):
		if len(args) > 1 or args[0] not in self.MENU_ITEMS:
			self.error(self.ERRORS.INVALID_CHOICE)
			return self.render_menu()

		opt = self.MENU_ITEMS[args[0]]
		return render_screen(opt[1],loan=self.state.loan)

	def render_menu(self):
		loan = self.state.loan
		self.print(f'Amount: {loan.amount}')
		self.print(f'Due On: {self.format_date(loan.date_due)}')
		for k, v in self.MENU_ITEMS.items():
			self.print(str(k) + ':',v[0])
		return self.CON

		

	def render(self, opt=None, *args):
		if opt is not None and not args:
			return self.handle_input(opt)
		if args:
			self.print('Invalid choice.')
		return self.render_menu()
	
class LoansPayAllScreen(UssdScreen, ScreenMixin):
	
	

	class Meta:
		label = 'pay'



	def handle_input(self, *args):
		pass

	def render_menu(self):
		loan = self.state.loan
		helpers.create_checkout(amount=loan.amount,ref_no=loan.application.code,msisdn=self.session.msisdn)
		

		self.print('Check your phone and Enter your Mpesa PIN to complete')
		return self.END

		

	def render(self, opt=None, *args):
		if opt is not None and not args:
			return self.handle_input(opt)
		if args:
			self.print('Invalid choice.')
		return self.render_menu()

class LoansPartScreen(UssdScreen, ScreenMixin):
	
	

	class Meta:
		label = 'pay_part'



	def handle_input(self, opt):
		try:
			amount = int(opt)
		except:
			self.print('Incorrect Amount')
			self.print('Enter Amount')
			return self.CON
		else:
			helpers.create_checkout(
				amount=amount,
				ref_no=self.state.loan.application.code,
				msisdn=self.session.phone_number)
			self.print('Check your phone and Enter your Mpesa PIN to complete')
			return self.END

	def render_menu(self):
		self.print('Enter Amount')
		return self.CON

		

	def render(self, opt=None, *args):
		if opt is not None and not args:
			return self.handle_input(opt)
		if args:
			self.print('Invalid choice.')
		return self.render_menu()
		