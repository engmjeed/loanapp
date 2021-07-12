
from django.conf.urls import url
from django.urls import path,include
from .views import KenyaSafaricomUssdView, GhanaMtnUssdView


urlpatterns=[
	path('', KenyaSafaricomUssdView.as_view(), name='ke_saf_ussd'),
]