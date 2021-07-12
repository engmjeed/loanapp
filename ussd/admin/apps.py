from django.apps import AppConfig


class UssdAdminConfig(AppConfig):
	name = 'ussd.admin'
	label = 'ussd_admin'

	def ready(self):
		pass
