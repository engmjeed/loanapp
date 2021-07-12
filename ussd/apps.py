from django.apps import AppConfig


class UssdConfig(AppConfig):
	name = 'ussd'

	def ready(self):
		from . import receivers
