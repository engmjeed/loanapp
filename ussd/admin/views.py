from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework import permissions

from ..models import SportMenuItem
from .serializers import SportMenuSerializer


class ListCreateSportMenuItem(ListCreateAPIView):

	permission_classes = (permissions.IsAuthenticated,)

	queryset = SportMenuItem.objects
	serializer_class = SportMenuSerializer
	filter_fields = ('sport', 'is_active')


class RetrieveUpdateDestroySportMenuItem(RetrieveUpdateDestroyAPIView):

	permission_classes = (permissions.IsAuthenticated,)

	queryset = SportMenuItem.objects
	serializer_class = SportMenuSerializer
