"""myproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin

from .views import (
    index, 
    clients,
    ChartData, 
    Check, 
    LatestPurchase,
    LatestClient,
    LoadDefaultClients
)
urlpatterns = [
    url(r'^$', index, name = "index"),
    url(r'^clients/$', clients, name = "clients"),
    url(r'^api/transaction/$', LatestPurchase.as_view()),
    url(r'^api/transaction/(?P<page>[0-9]+)/$', LatestPurchase.as_view()),
    url(r'^api/check/$', Check.as_view()),
    url(r'^api/clients/$', LoadDefaultClients.as_view()),
    url(r'^api/clients/(?P<type>[a-z]+)/$', LatestClient.as_view()),
    url(r'^api/clients/(?P<type>[a-z]+)/(?P<page>[0-9]+)/$', LatestClient.as_view()),
]
