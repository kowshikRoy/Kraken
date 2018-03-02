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
    productIndex,
    salesmanIndex,
    clientIndex,
    regionIndex,
    clients,
    ChartData,
    Check,
    LatestPurchase,
    LatestClient,
    LoadDefaultClients,
    loginView,
    logoutView,
    test,
    ProductView,
    ClientView,
    RegionView,
    SalesManView,
    product,
    client,
    region,
    salesman,
    LoadProduct,
    Percentile,
    DefaultView,
    CompareView,

)
urlpatterns = [
    url(r'^test/$', test),
    url(r'^$', index, name = "index"),
    url(r'^products/$', productIndex, name = "products"),
    url(r'^clients/$', clientIndex, name = "clients"),
    url(r'^regions/$', regionIndex, name = "regions"),
    url(r'^salesmans/$', salesmanIndex, name = "salesmans"),
    url(r'^login/',loginView, name= "login"),
    url(r'^logout/', logoutView, name= "logout"),
    url(r'^p/(?P<id>[0-9]+)/$', product, name= 'product'),
    url(r'^c/(?P<id>[0-9]+)/$', client, name= 'client'),
    url(r'^r/(?P<id>[0-9]+)/$', region, name= 'region'),
    url(r'^s/(?P<id>[0-9]+)/$', salesman, name= 'salesman'),
    url(r'^cients/$', clients, name = "clientsView"),
    url(r'^api/default/$', DefaultView.as_view()),
    url(r'^api/compare/$', CompareView.as_view()),
    url(r'^api/Product/$', ProductView.as_view()),
    url(r'^api/Client/$', ClientView.as_view()),
    url(r'^api/Region/$', RegionView.as_view()),
    url(r'^api/SalesMan/$', SalesManView.as_view()),
    url(r'^api/LoadProduct/$', LoadProduct.as_view()),
    url(r'^api/percentile/$', Percentile.as_view()),
    url(r'^api/transaction/$', LatestPurchase.as_view()),
    # url(r'^api/Lransaction/(?P<page>[0-9]+)/$', LatestPurchase.as_view()),
    # url(r'^api/check/$', Check.as_view()),
    url(r'^api/clients/$', LoadDefaultClients.as_view()),
    url(r'^api/clients/(?P<type>[a-z]+)/$', LatestClient.as_view()),
    url(r'^api/clients/(?P<type>[a-z]+)/(?P<page>[0-9]+)/$', LatestClient.as_view()),
]
