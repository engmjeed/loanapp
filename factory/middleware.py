from ipware import get_client_ip
from .models import IPWhitelist
from django.conf import settings


#IP Throttle
class IpThrotterMiddleware:
	def __init__(self, get_response):
		self.get_response = get_response


	def is_ip_in_whitelist(self,client_ip):
		return IPWhitelist.objects.filter(ip_address=client_ip).exists()

	def __call__(self, request):
		client_ip, is_routable = get_client_ip(request)

		if client_ip is None:
			raise ValueError(
				'Acess  not allowed'
			)

		else:


			if not settings.DEBUG and not self.is_ip_in_whitelist(client_ip):

				raise ValueError(
					'Acess  not allowed.'
				)



		response = self.get_response(request)



		return response
