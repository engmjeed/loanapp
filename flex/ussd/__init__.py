
#Loads the void module
def _load_void():
	from .utils import void
_load_void()
del _load_void

from .namespaces import ussd_namespace

default_app_config = 'flex.ussd.apps.UssdConfig'


def get_screen(name, *args, **kwargs):
	from .screens import get_screen
	return get_screen(name, *args, **kwargs)


