"""loanapp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from authentication.views import obtain_expiring_auth_token


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/charges/', include('charges.urls')),
    path('api/v1/funds/', include('funds.urls')),
    path('api/v1/products/', include('products.urls')),
    path('api/v1/ipn/', include('payments.urls')),
    path('api/v1/organisations/', include('organisations.urls')),
    path('api/v1/clients/', include('clients.urls')),
    path('api/v1/loans/', include('loans.urls')),
    path('ussd/', include('ussd.urls')),
    # path('api-auth/', include('rest_framework.urls')),
    path('api/v1/authenticate/',obtain_expiring_auth_token,name='authenticate'),

]
# Text to put at the end of each page's < title > .
admin.site.site_title = 'Jijenge Loans Admin'

# Text to put in each page's <h1> (and above login form).
admin.site.site_header = 'Jijenge Loans Admin'

# Text to put at the top of the admin index page.
admin.site.index_title = 'Jijenge Loans'
