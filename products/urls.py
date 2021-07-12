from django.contrib import admin
from django.urls import path,include
from . import views


urlpatterns = [
    path('', views.ProductsViewSet.as_view()),
    path('<int:pk>', views.ProductsViewSet.as_view()),
    
    
]
