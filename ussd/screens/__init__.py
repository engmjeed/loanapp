from collections import OrderedDict

from flex.ussd.screens import UssdScreen, render_screen
from ast import literal_eval
from django.conf import settings


from . import loan,account
from .mixins import ScreenMixin
from clients.models import Client
# from .helpers import Fetcher
# fetcher = Fetcher()



class InitialScreen(UssdScreen, ScreenMixin):

	class Meta:
		label = 'initial'

	def render(self, opt=None, *args):
		if self.is_client():
			phone_field = self.msisdn_to_phonefield()
			client = Client.objects.get(msisdn=phone_field)
			self.session.client = client
			return render_screen('jl.home')
		else:
			return render_screen('jl.unknownmous_user')

	def is_client(self):
		phone_field = self.msisdn_to_phonefield()
		
		return Client.objects.filter(is_active=True,msisdn=phone_field).exists()
			


class HomeScreen(UssdScreen, ScreenMixin):
	
	nav_menu = None
	MENU_ITEMS = OrderedDict([
	('1', ("Request Loan", "jl.products")),
	('2', ("Repay Loan", "jl.my_loans")),
	('3', ("My Account", "jl.my_account_home")),
	# ('4', ("Activate", "jl.not_implemented")),	
])

	class Meta:
		label = 'home'


	def handle_input(self, *args):
		if len(args) > 1 or args[0] not in self.MENU_ITEMS:
			self.error(self.ERRORS.INVALID_CHOICE)
			return self.render_menu()

		opt = self.MENU_ITEMS[args[0]]
		
		return render_screen(opt[1])

	def render_menu(self):
		self.print(f"{self.time_salutation()} {self.session.client.first_name}, Welcome to {settings.BRAND_NAME}")
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

class UnknownmousUserScreen(UssdScreen, ScreenMixin):
	nav_menu = None

	class Meta:
		label = 'unknownmous_user'



	def handle_input(self, *args):
		pass

	def render_menu(self):
		self.print("You are here For a Loan But you are not a client!")
		
		return self.CON

	def get_menu(self):
		pass
		
	def render(self, opt=None, *args):
		if opt is not None and not args:
			return self.handle_input(opt)
		if args:
			self.print('Invalid choice.')
		return self.render_menu()


class NotImplementedScreen(UssdScreen, ScreenMixin):
	

	class Meta:
		label = 'not_implemented'



	def handle_input(self, *args):
		pass

	def render_menu(self):
		self.print("We will be working soon. relax")
		
		return self.CON

	def get_menu(self):
		pass
		
	def render(self, opt=None, *args):
		if opt is not None and not args:
			return self.handle_input(opt)
		if args:
			self.print('Invalid choice.')
		return self.render_menu()








