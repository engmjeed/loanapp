from django.contrib import admin
from django.urls import path,include
from . import views


urlpatterns = [
    path('', views.OrganisationsViewSet.as_view()),
    path('<int:pk>', views.OrganisationsViewSet.as_view()),
    path('centers', views.CentersViewSet.as_view()),
    path('centers/<int:pk>', views.CentersViewSet.as_view()),
    
    
]
