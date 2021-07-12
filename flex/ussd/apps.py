import os
from importlib import import_module
from django.utils.module_loading import module_has_submodule
from django.apps import AppConfig, apps
from django.conf import settings

from . import settings as ussd_settings

SCREENS_MODULE_NAME = 'screens'


class UssdConfig(AppConfig):
	name = 'flex.ussd'
	label = 'flex_ussd'

	def ready(self):
		self.check_data_dir()
		self.load_screen_modules()

	def check_data_dir(self):
		if not os.path.exists(settings.LOCAL_DATA_DIR):
			os.mkdir(settings.LOCAL_DATA_DIR)
			svn_content = """*
			!.gitignore"""
			with open(os.path.join(settings.LOCAL_DATA_DIR, '.gitignore'), 'w+') as f:
				f.write(svn_content)

	def load_screen_modules(self):
		for appconfig in apps.get_app_configs():
			if module_has_submodule(appconfig.module, SCREENS_MODULE_NAME):
				import_module('%s.%s' % (appconfig.name, SCREENS_MODULE_NAME))

