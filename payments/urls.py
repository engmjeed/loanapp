from django.contrib import admin
from django.urls import path,include
from . import views


urlpatterns = [
    path('payins', views.Payins.as_view()),
    path('payout-response', views.PayoutResponse.as_view()),
    
]
