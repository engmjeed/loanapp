from django.contrib import admin
from django.urls import path,include
from . import views


urlpatterns = [
    path('', views.ClientsViewSet.as_view()),
    path('<int:pk>', views.ClientsViewSet.as_view()),
    path('loan-profiles', views.ClientLoanProfilesViewSet.as_view()),
    path('loan-profiles/<int:pk>', views.ClientLoanProfilesViewSet.as_view()),
    
    
    
]
