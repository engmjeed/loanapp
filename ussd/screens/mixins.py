from collections import OrderedDict, Mapping

from flex.ussd.screens import UssdScreen
from flex.ussd.screens import render_screen
from utils.decorators import cached_property
from phonenumber_field.phonenumber import to_python
from django.utils import timezone

from django.conf import settings




class ScreenMixin(object):

	def format_date(self,date):
		format = "%d/%m/%Y"
		return date.strftime(format)
	
	def time_salutation(self):
		now = timezone.now()
		if now.hour < 12:
			return 'Good Morning'

		elif 12 <= now.hour < 18:
			return 'Good Afternoon'
		else:
			return'Good Evening'


		
	def msisdn_to_phonefield(self):
		return to_python(self.session.msisdn)

class RestoreSessionMixin(object):

	restore_session_message = 'Your previous session is still active.'

	restore_session_options = OrderedDict([
		('1', ('Resume', 'resume_session')),
		('2', ('Discard', 'cancel_restoration')),
	])


	def can_restore_session(self):
		return True

	def get_restore_session_options(self):
		rv = self.restore_session_options
		assert isinstance(rv, Mapping), (
			"Screen <%s: '%s'> should either define a Mapping on the"
			" `restore_session_options` attribute or override the"
			" `get_restore_session_options()` method."
			% (self.__class__.__name__, self.name)
		)
		return rv

	def print_restore_session_message(self):
		self.print(self.restore_session_message or '')

	def print_restore_session_menu(self):
		for k, v in (self.get_restore_session_options() or {}).items():
			self.print(k,v[0])

	def render_restore_session_prompt(self):
		self.nav_menu = None
		self.print_restore_session_message()
		self.print_restore_session_menu()
		return self.CON

	def handle_restore_session_prompt(self, opt):
		options = self.get_restore_session_options()

		if opt not in options:
			self.error(self.ERRORS.INVALID_CHOICE)
			return self.render_restore_session_prompt()

		txt, fn, reset, *_ = tuple(options[opt]) + (True,)

		if isinstance(fn, str):
			fn = getattr(self, fn)

		assert callable(fn) and not isinstance(fn, type), (
			'Restore session callback must be a function or callable object. Got '
			'%r in <%s: %r>.' % (type(fn), self.__class__.__name__, self.name)
		)

		reset and self.session.reset_restored()
		return fn()

	def resume_session(self):
		return self.render()

	def restore(self, *args):
		if not self.can_restore_session():
			return self.cancel_restoration(*args)
		elif args:
			return self.handle_restore_session_prompt(args[0])
		else:
			return self.render_restore_session_prompt()
	
	






