import re
import json
import requests
from ipware import get_client_ip
from django.conf import settings
from django.http import HttpResponse
from requests.exceptions import Timeout as RequestTimeout

from flex.ussd.middleware import UssdMiddleware

try:
	import simplejson
	JSONDecodeErrors = (json.JSONDecodeError, simplejson.JSONDecodeError)
except ImportError:
	JSONDecodeErrors = (json.JSONDecodeError,)


class KenyaSafaricomUssdMiddleware(UssdMiddleware):
	"""Middleware for USSD requests from Safaricom Kenya."""

	def extract_request_data(self, req):
		rv = dict(req.GET.items())
		rv.setdefault('phone_number', rv.get('msisdn'))
		

		
		return rv

	def prepare_request(self, request):
		super().prepare_request(request)
		request.ussd_session.country_code = 'KE'

	# def teardown_request(self, req, res):
	# 	res = super().teardown_request(req, res) or res
	# 	if hasattr(res, 'type') and isinstance(res.content, (str, bytes)):
	# 		res.content = (res.type+' ').encode()+res.content
	# 	return res





_STRIP_USSD_CODE_RE = re.compile(r'(?:^\*)|(?:\#$)')

def strip_ussd_code(code):
	return code and _STRIP_USSD_CODE_RE.sub('', code)


class GhanaMtnUssdMiddleware(UssdMiddleware):
	"""Middleware for USSD requests from MTN Ghana."""

	@property
	def api_url(self):
		return settings.GHANA_CLOUD_AFRICA_API_URL

	@property
	def api_service_token(self):
		return settings.GHANA_CLOUD_AFRICA_API_SERVICE_TOKEN

	def prepare_request(self, request):
		super().prepare_request(request)
		request.ussd_session.country_code = 'GH'

	def extract_request_data(self, req):
		rv = json.loads(req.body.decode()) if req.body else {}
		rv['service_code'] = strip_ussd_code(rv.get('ussd_code')) or None
		if 'user_request' in rv:
			if str(rv.get('type', '')).lower() == 'initiation':
				rv['request_inputs'] = strip_ussd_code(rv['user_request'])
				if rv['service_code']:
					rv['request_inputs'] = rv['request_inputs'][len(rv['service_code']):]
			else:
				rv['request_inputs'] = rv['user_request']
		return rv

	def teardown_request(self, req, res):
		res = super().teardown_request(req, res) or res
		res_type, body = res.content.decode('utf-8').split(' ',1)
		res.content = body

		url = '%s/api/ussdclientresponse' % (self.api_url,)
		payload = dict(
			service_token=self.api_service_token,
			ussd_code='*%s' % (req.ussd_data['service_code']),
			phone_number=req.ussd_data['phone_number'],
			message=res.content,
			type=res_type
		)

		rv = False
		for con_timeout in (4, 6, 8, 8):
			try:
				r = requests.post(url, json=payload, timeout=(con_timeout, 16))
			except RequestTimeout:
				continue
			else:
				if r.status_code == 200:
					try:
						rj = r.json()
					except JSONDecodeErrors:
						continue
					else:
						rv = isinstance(rj, dict) and rj.get('status_code:') == 200
						if rv:
							break
		return res if rv else HttpResponse('Error %s' % (r.text if r and settings.DEBUG else ''))



#IP Throttle
class IpThrotterMiddleware:
	def __init__(self, get_response):
		self.get_response = get_response

	def is_ussd_path(self,request):
		return '/ussd/' in request.path

	def __call__(self, request):
		client_ip, is_routable = get_client_ip(request)

		if client_ip is None:
			raise ValueError(
				'Acess  not allowed for USSD endpoint'
			)

		else:

			if not settings.DEBUG and client_ip not in settings.ALLOWED_CLIENTS and self.is_ussd_path(request):
				data={'ip':client_ip}
				
				raise ValueError(
					'Acess  not allowed for USSD endpoint'
				)



		response = self.get_response(request)



		return response
