from django.conf import settings
import os,sys
import django

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'loanapp.settings')
django.setup()

class Env:
    pass