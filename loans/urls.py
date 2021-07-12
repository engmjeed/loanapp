from django.contrib import admin
from django.urls import path,include
from . import views


urlpatterns = [
    path('', views.LoanViewSet.as_view()),
    path('<int:pk>', views.LoanViewSet.as_view()),
    path('applications', views.LoanApplicationsViewSet.as_view()),
    path('applications/<int:pk>', views.LoanApplicationsViewSet.as_view()),
    
    
    
    
]
