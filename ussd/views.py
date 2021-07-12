from django.shortcuts import render
from flex.ussd.views import UssdView
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
from .middleware import KenyaSafaricomUssdMiddleware, GhanaMtnUssdMiddleware


@method_decorator(KenyaSafaricomUssdMiddleware, 'dispatch')
class KenyaSafaricomUssdView(UssdView):
	pass



@method_decorator((csrf_exempt, GhanaMtnUssdMiddleware), 'dispatch')
class GhanaMtnUssdView(UssdView):
	pass