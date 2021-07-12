
from django.conf.urls import url
from . import views as vw


urlpatterns=[
	url(r'^screens/sports-menu/$', vw.ListCreateSportMenuItem.as_view(), name='sports_menu'),
	url(r'^screens/sports-menu/(?P<pk>[0-9]+)/$',
		vw.RetrieveUpdateDestroySportMenuItem.as_view(), name='sports_menu'),
]
