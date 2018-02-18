import time
import math
import json
from datetime import date,timedelta,datetime

from django.shortcuts import render,redirect,get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate,logout


from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response

from .utils import proper_paginate, getPercentile,getData
from .models import  Region, Product, Client, SalesMan,Transaction,Voucher

pageint = 5
dic = {}
serial = []
pairs = []

def cmp(client):
		return dic[client]

def test(request):
	qs		= Transaction.objects.filter(product__company = request.user.profile.company)
	return render(request, 'main/test.html', {'items': qs})

@login_required
def index(request):
	return render(request , 'main/index.html', {
		'products': Product.objects.filter(company = request.user.profile.company ),
		'clients': Client.objects.filter(company = request.user.profile.company),
		'regions': Region.objects.all(),
		'salesMans': SalesMan.objects.filter(company = request.user.profile.company)
	})


def product(request,*args, **kwargs):
	product = get_object_or_404(Product.objects.filter(company = request.user.profile.company), pk =kwargs['id'])
	return render(request, 'main/product.html', {'product': product})


def client(request,*args, **kwargs):
	client = get_object_or_404(Client, pk =kwargs['id'])
	return render(request, 'main/client.html', {'client': client})

def region(request,*args, **kwargs):
	region = get_object_or_404(Region, pk =kwargs['id'])
	return render(request, 'main/region.html', {'region': region})

def salesman(request,*args, **kwargs):
	salesman = get_object_or_404(SalesMan, pk =kwargs['id'])
	return render(request, 'main/salesman.html', {'salesman': salesman})

def predict(request, *args, **kwargs):
	volume = {}
	tk = {}
	label = []

	for i in range(yearMin, yearMax + 1):
		label.append(i)
		volume[i] = 0
		tk[i] = 0

	for t in transactions:
		year  = t.voucher.date.year;
		tk[year] += t.amount
		volume[year] += t.volume





class ProductView(APIView):
	authentication_classes 	= (SessionAuthentication, BasicAuthentication)
	permission_classes 		= (IsAuthenticated,)

	def get(self, request, *args, **kwargs) :
		print(request.GET)

		beginDate 	= datetime.strptime( '1900-01-01','%Y-%m-%d').date()
		endDate 	= date.today()

		if request.GET['beginDate'] != '':
			beginDate 	= datetime.strptime(request.GET.get('beginDate', '1900-01-01'),'%Y-%m-%d').date()
		if request.GET['endDate'] != '':
			endDate 	= datetime.strptime(request.GET.get('endDate', '1900-01-01'),'%Y-%m-%d').date()

		transactions		= Transaction.objects.filter(product__company = request.user.profile.company,
			voucher__date__gte = beginDate, voucher__date__lte = endDate
		)

		if request.GET['client'] != '':
			transactions	= transactions.filter(voucher__client__id = request.GET['client'])
		if request.GET['region'] != '':
			transactions 	= transactions.filter(voucher__client__region__id = request.GET['region'])
		if request.GET['salesman'] != '':
			transactions 	= transactions.filter(seller__id = request.GET['salesman'])

		products			= Product.objects.filter(company = request.user.profile.company)
		MapforVolume 	= {}
		MapForTk		= {}
		for p in products:
			MapforVolume[p.id] = 0
			MapForTk[p.id] = 0

		for i in transactions:
			MapForTk[i.product.id] += i.amount
			MapforVolume[i.product.id] += i.volume
			print(i.seller.id)


		output 		= [(p, MapforVolume[p.id], MapForTk[p.id]) for p in products]
		if request.GET['queryType'] == 'volume':
			output = sorted(output, key = lambda x: x[1], reverse = True)
		elif request.GET['queryType'] == 'tk':
			output = sorted(output, key = lambda x: x[2], reverse = True)


		# return Response(getData(request, output, 10, request.GET.get('page', 1), 'main/includes/product-table.html'))
		paginator = Paginator(output, pageint	)
		page = request.GET.get('page', 1)
		pg = proper_paginate(paginator, int(page))
		

		try:
			rows = paginator.page(page)
		except PageNotAnInteger:
			rows = paginator.page(1)
		except EmptyPage:
			rows = paginator.page(paginator.num_pages)


		data = {
			'table': render_to_string('main/includes/product-table.html', {'transaction': rows, 'page-page_range': pg}),
			'paginator': render_to_string('main/includes/Paginator.html', {'page': rows, 'page_range': pg, 'id': "Product-" + request.GET['queryType']})
		}
		return Response(data)


class ClientView(APIView):
	authentication_classes 	= (SessionAuthentication, BasicAuthentication)
	permission_classes 		= (IsAuthenticated,)

	def get(self, request, *args, **kwargs) :

		beginDate 	= datetime.strptime( '1900-01-01','%Y-%m-%d').date()
		endDate 	= date.today()

		if request.GET['beginDate'] != '':
			beginDate 	= datetime.strptime(request.GET.get('beginDate', '1900-01-01'),'%Y-%m-%d').date()
		if request.GET['endDate'] != '':
			endDate 	= datetime.strptime(request.GET.get('endDate', '1900-01-01'),'%Y-%m-%d').date()

		transactions		= Transaction.objects.filter(product__company = request.user.profile.company,
			voucher__date__gte = beginDate, voucher__date__lte = endDate
		)

		if request.GET['product'] != '':
			transactions	= transactions.filter(product__id = request.GET['product'])
		if request.GET['region'] != '':
			transactions 	= transactions.filter(voucher__client__region__id = request.GET['region'])
		if request.GET['salesman'] != '':
			transactions 	= transactions.filter(seller__id = request.GET['salesman'])

		clients			= Client.objects.filter(company = request.user.profile.company)
		MapforVolume 	= {}
		MapForTk		= {}
		for c in clients:
			MapforVolume[c.id] = 0
			MapForTk[c.id] = 0

		for i in transactions:
			MapForTk[i.voucher.client.id] += i.amount
			MapforVolume[i.voucher.client.id] += i.volume


		output 		= [(c, MapforVolume[c.id], MapForTk[c.id]) for c in clients]
		if request.GET['queryType'] == 'volume':
			output = sorted(output, key = lambda x: x[1], reverse = True)
		elif request.GET['queryType'] == 'tk':
			output = sorted(output, key = lambda x: x[2], reverse = True)

		paginator = Paginator(output, pageint)
		page = request.GET.get('page', 1)
		pg = proper_paginate(paginator, int(page))

		try:
			rows = paginator.page(page)
		except PageNotAnInteger:
			rows = paginator.page(1)
		except EmptyPage:
			rows = paginator.page(paginator.num_pages)


		data = {
			'table': render_to_string('main/includes/client-table.html', {'objects': rows, 'page-page_range': pg}),
			'paginator': render_to_string('main/includes/Paginator.html', {'page': rows, 'page_range': pg, 'id': "Client-" + request.GET['queryType']})
		
		}
		return Response(data)

class RegionView(APIView):
	authentication_classes 	= (SessionAuthentication, BasicAuthentication)
	permission_classes 		= (IsAuthenticated,)

	def get(self, request, *args, **kwargs) :

		beginDate 	= datetime.strptime( '1900-01-01','%Y-%m-%d').date()
		endDate 	= date.today()

		if request.GET['beginDate'] != '':
			beginDate 	= datetime.strptime(request.GET.get('beginDate', '1900-01-01'),'%Y-%m-%d').date()
		if request.GET['endDate'] != '':
			endDate 	= datetime.strptime(request.GET.get('endDate', '1900-01-01'),'%Y-%m-%d').date()

		transactions		= Transaction.objects.filter(product__company = request.user.profile.company,
			voucher__date__gte = beginDate, voucher__date__lte = endDate
		)

		if request.GET['product'] != '':
			transactions	= transactions.filter(product__id = request.GET['product'])
		if request.GET['client'] != '':
			transactions 	= transactions.filter(voucher__client__id = request.GET['client'])
		if request.GET['salesman'] != '':
			transactions 	= transactions.filter(seller__id = request.GET['salesman'])

		regions			= Region.objects.all()
		MapforVolume 	= {}
		MapForTk		= {}
		for r in regions:
			MapforVolume[r.id] = 0
			MapForTk[r.id] = 0

		for i in transactions:
			MapForTk[i.voucher.client.region.id] += i.amount
			MapforVolume[i.voucher.client.region.id] += i.volume


		output 		= [(r, MapforVolume[r.id], MapForTk[r.id]) for r in regions]
		if request.GET['queryType'] == 'volume':
			output = sorted(output, key = lambda x: x[1], reverse = True)
		elif request.GET['queryType'] == 'tk':
			output = sorted(output, key = lambda x: x[2], reverse = True)

		paginator = Paginator(output, pageint)
		page = request.GET.get('page', 1)
		pg = proper_paginate(paginator, int(page))

		try:
			rows = paginator.page(page)
		except PageNotAnInteger:
			rows = paginator.page(1)
		except EmptyPage:
			rows = paginator.page(paginator.num_pages)


		data = {
			'table': render_to_string('main/includes/region-table.html', {'objects': rows, 'page-page_range': pg}),
			'paginator': render_to_string('main/includes/Paginator.html', {'page': rows, 'page_range': pg, 'id': "Region-" + request.GET['queryType']})
		
		
		}
		return Response(data)

class SalesManView(APIView):
	authentication_classes 	= (SessionAuthentication, BasicAuthentication)
	permission_classes 		= (IsAuthenticated,)

	def get(self, request, *args, **kwargs) :

		beginDate 	= datetime.strptime( '1900-01-01','%Y-%m-%d').date()
		endDate 	= date.today()

		if request.GET['beginDate'] != '':
			beginDate 	= datetime.strptime(request.GET.get('beginDate', '1900-01-01'),'%Y-%m-%d').date()
		if request.GET['endDate'] != '':
			endDate 	= datetime.strptime(request.GET.get('endDate', '1900-01-01'),'%Y-%m-%d').date()

		transactions		= Transaction.objects.filter(product__company = request.user.profile.company,
			voucher__date__gte = beginDate, voucher__date__lte = endDate
		)

		if request.GET['product'] != '':
			transactions	= transactions.filter(product__id = request.GET['product'])
		if request.GET['client'] != '':
			transactions 	= transactions.filter(voucher__client__id = request.GET['client'])
		if request.GET['region'] != '':
			transactions 	= transactions.filter(voucher__client__region__id = request.GET['region'])

		salesMans			= SalesMan.objects.filter(company = request.user.profile.company)
		MapforVolume 	= {}
		MapForTk		= {}
		for r in salesMans:
			MapforVolume[r.id] = 0
			MapForTk[r.id] = 0

		for i in transactions:
			MapForTk[i.seller.id] += i.amount
			MapforVolume[i.seller.id] += i.volume


		output 		= [(r, MapforVolume[r.id], MapForTk[r.id]) for r in salesMans]
		if request.GET['queryType'] == 'volume':
			output = sorted(output, key = lambda x: x[1], reverse = True)
		elif request.GET['queryType'] == 'tk':
			output = sorted(output, key = lambda x: x[2], reverse = True)


		paginator = Paginator(output, pageint)
		page = request.GET.get('page', 1)
		pg = proper_paginate(paginator, int(page))

		try:
			rows = paginator.page(page)
		except PageNotAnInteger:
			rows = paginator.page(1)
		except EmptyPage:
			rows = paginator.page(paginator.num_pages)


		data = {
			'table': render_to_string('main/includes/salesman-table.html', {'objects': rows, 'page-page_range': pg}),
			'paginator': render_to_string('main/includes/Paginator.html', {'page': rows, 'page_range': pg, 'id': "SalesMan-" + request.GET['queryType']})
		}
		return Response(data)

class LoadProduct(APIView):
	authentication_classes 	= (SessionAuthentication, BasicAuthentication)
	permission_classes 		= (IsAuthenticated,)

	def get(self, request, *args, **kwargs) :
		transactions		= Transaction.objects.filter(product__company = request.user.profile.company,)
		if request.GET['product'] != '':
			transactions 	= transactions.filter(product__id = request.GET['product'])

		data = {}
		yearMin = date.today().year
		yearMax = date.today().year

		# Season Data
		volume = {}
		tk = {}
		label = []

		for i in range(1,13):
			label.append(date(2012,i,1).strftime('%b'))
			volume[i] = 0
			tk[i] = 0

		for t in transactions:
			mon = t.voucher.date.month;
			tk[mon] += t.amount
			volume[mon] += t.volume
			yearMin = min(yearMin, t.voucher.date.year)
			yearMax = max(yearMax, t.voucher.date.year)

		data['season'] = {
			'label'		: label,
			'volume' 	: [volume[i] for i in range(1, 13)],
			'tk'		: [tk[i] for i in range(1,13)]
		}


		#Year Data

		volume = {}
		tk = {}
		label = []

		for i in range(yearMin, yearMax + 1):
			label.append(i)
			volume[i] = 0
			tk[i] = 0

		for t in transactions:
			year  = t.voucher.date.year;
			tk[year] += t.amount
			volume[year] += t.volume


		data['year'] = {
			'label'		: label,
			'volume' 	: [volume[i] for i in range(yearMin, yearMax + 1)],
			'tk'		: [tk[i] for i in range(yearMin,yearMax + 1)]
		}

		#This Year Data
		beginDate = date.today().replace(year = date.today().year-1, day = 1)
		transactions = transactions.filter(voucher__date__gte = beginDate)

		volume = {}
		tk = {}
		label = []
		temp = beginDate
		print(temp)
		for i in range(13):
			out = temp.strftime('%b %Y');
			label.append(out)
			volume[out] = 0
			tk[out] = 0
			temp += timedelta(days = 32)
			print(out)

		for t in transactions:
			out  = t.voucher.date.strftime('%b %Y')
			tk[out] += t.amount
			volume[out] += t.volume

		data['onlyThisYear'] = {
			'label'		: label,
			'volume' 	: [volume[i] for i in label],
			'tk'		: [tk[i] for i in label]
		}

		return Response(data)

class PercentileProduct(APIView):
	authentication_classes 	= (SessionAuthentication, BasicAuthentication)
	permission_classes 		= (IsAuthenticated,)

	def get(self, request, *args, **kwargs) :
		transactions		= Transaction.objects.filter(product__company = request.user.profile.company,)
		products			= Product.objects.filter(company = request.user.profile.company)


		tk = {}
		label = []

		for i in range(1,100,20):
			label.append(str(i)+"-"+str(i+19)+'%')
		for p in products: tk[p.id] = 0
		for t in transactions: tk[t.product.id] += t.amount
		output = [( p , tk[p.id]) for p in products]
		output = sorted(output, key = lambda x: x[1], reverse = True)


		data = {
			'label' : label,
			'data'	: getPercentile(output, 5),
		}

		return Response(data)


class PercentileClient(APIView):
	authentication_classes 	= (SessionAuthentication, BasicAuthentication)
	permission_classes 		= (IsAuthenticated,)

	def get(self, request, *args, **kwargs) :
		transactions		= Transaction.objects.filter(product__company = request.user.profile.company,)
		clients				= Client.objects.filter(company = request.user.profile.company)


		tk = {}
		label = []

		for i in range(1,100,20):
			label.append(str(i)+"-"+str(i+19)+'%')

		for p in clients: tk[p.id] = 0
		for t in transactions: tk[t.voucher.client.id] += t.amount
		output = [( p , tk[p.id]) for p in clients]
		output = sorted(output, key = lambda x: x[1], reverse = True)

		data = {
			'label' : label,
			'data'	: getPercentile(output, 5),
		}

		print(label)


		return Response(data)

class PercentileRegion(APIView):
	authentication_classes 	= (SessionAuthentication, BasicAuthentication)
	permission_classes 		= (IsAuthenticated,)

	def get(self, request, *args, **kwargs) :
		transactions		= Transaction.objects.filter(product__company = request.user.profile.company,)
		regions 			= Region.objects.all()
		data = {}

		tk = {}
		label = []

		for i in range(1,100,20):
			label.append(str(i)+"-"+str(i+19)+'%')

		for r in regions: tk[r.id] = 0
		for t in transactions: tk[t.voucher.client.region.id] += t.amount

		output = [( p , tk[p.id]) for p in regions]
		output = sorted(output, key = lambda x: x[1], reverse = True)

		data = {
			'label' : label,
			'data'	: getPercentile(output, 5),
		}
		return Response(data)



class PercentileSalesMan(APIView):
	authentication_classes 	= (SessionAuthentication, BasicAuthentication)
	permission_classes 		= (IsAuthenticated,)

	def get(self, request, *args, **kwargs) :
		transactions		= Transaction.objects.filter(product__company = request.user.profile.company,)
		salesMans 			= SalesMan.objects.filter(company = request.user.profile.company)
		data = {}

		tk = {}
		label = []

		for i in range(1,100,20):
			label.append(str(i)+"-"+str(i+19)+'%')

		for r in salesMans: tk[r.id] = 0
		for t in transactions: tk[t.seller.id] += t.amount

		output = [( p , tk[p.id]) for p in salesMans]
		output = sorted(output, key = lambda x: x[1], reverse = True)

		data = {
			'label' : label,
			'data'	: getPercentile(output, 5),
		}

		return Response(data)


def clients(request):
	today 		= date.today()
	qs			= Transaction.objects.all()
	qyear		= qs.filter(voucher__date__gte = today.replace(month=1, day=1), voucher__date__lte = today)
	qmonth		= qs.filter(voucher__date__gte = today - timedelta(days = 30), voucher__date__lte = today)
	qweek		= qs.filter(voucher__date__gte = today - timedelta(days = 7) , voucher__date__lte = today)


	# begin & end
	weekBegin		= today - timedelta(days = 6)
	weekEnd			= today
	monthBegin 		= today - timedelta(days = 29)
	monthEnd		= today
	yearBegin		= today.replace(month = 1, day = 1)
	yearEnd			= today
	context		= {
		'weekBegin'			: weekBegin,
		'weekEnd'			: weekEnd,
		'monthBegin'		: monthBegin,
		'monthEnd'			: monthEnd,
		'yearBegin'			: yearBegin,
		'yearEnd'			: yearEnd,
	}
	return render(request, 'main/clients.html', context)


class ChartData(APIView):
	authentication_classes 	= []
	permission_classes 		= []
	def get(self, request, *args, **kwargs) :
		populate()

		paginator = Paginator(pairs, pageint)
		page = kwargs.get('page_id', 1)
		pg = proper_paginate(paginator, int(page))

		try:
			users = paginator.page(page)
		except PageNotAnInteger:
			users = paginator.page(1)
		except EmptyPage:
			users = paginator.page(paginator.num_pages)


		data = {
			'labels': [x.id for x,y in users],
			'data'	: [y for x,y in users],

		}
		return Response(data)

class Check(APIView):
	authentication_classes 	= []
	permission_classes 		= []

	def get(self, request, *args, **kwargs) :
		print(render(request,'main/base.html'))
		data = {
			'labels': [1,2,3,4],
			'data'	: [pageint,20,30,40],
			'div'	: render_to_string('main/index.html',),

		}
		return Response(data)


class LatestPurchase(APIView):
	authentication_classes 	= []
	permission_classes 		= []

	def get(self, request, *args, **kwargs) :

		page 	= kwargs.get('page',1)
		qs		= Transaction.objects.all()
		latest  = qs.order_by('-voucher__date')
		paginator = Paginator(latest, pageint)
		page = kwargs.get('page', 1)
		pg = proper_paginate(paginator, int(page))

		try:
			users = paginator.page(page)
		except PageNotAnInteger:
			users = paginator.page(1)
		except EmptyPage:
			users = paginator.page(paginator.num_pages)

		print(users)
		data = {
			'LatestPurchase': render_to_string('main/includes/transactiontable.html', {'transaction': users,}),
			'latestPaginator': render_to_string('main/includes/Paginator.html', {'page': users, 'page_range': pg })

		}
		return Response(data)


class LatestClient(APIView):
	authentication_classes 	= []
	permission_classes 		= []

	def get(self, request, *args, **kwargs) :
		today = date.today()
		table 	= kwargs['type']
		if(table == None):
			return None

		query = []
		if table == 'week':
			query	= Transaction.objects.filter(voucher__date__gte = today - timedelta(days = 7) , voucher__date__lte = today)
		elif table == 'month':
			query	= Transaction.objects.filter(voucher__date__gte = today - timedelta(days = 30), voucher__date__lte = today)
		else:
			query	= Transaction.objects.filter(voucher__date__gte = today.replace(month=1, day=1), voucher__date__lte = today)

		for c in Client.objects.all():dic[c] = 0
		for i in query:dic[i.voucher.client] += i.amount
		serial 		= sorted(Client.objects.all(), key=cmp, reverse = True)
		yearTable 	= [(i, dic[i])  for i in serial]
		yearData	= [ dic[i] for i in serial]

		paginator = Paginator(yearTable, pageint)
		page = kwargs.get('page', 1)
		pg = proper_paginate(paginator, int(page))

		try:
			pageYear = paginator.page(page)
		except PageNotAnInteger:
			pageYear = paginator.page(1)
		except EmptyPage:
			pageYear = paginator.page(paginator.num_pages)


		data = {
			'Table'		: render_to_string('main/includes/clientTable.html', {'page' : pageYear}),
			'Data'		: yearData[pageYear.start_index()-1: pageYear.end_index()],
			'Labels'	: [' ']*(pageYear.end_index()- pageYear.start_index() + 1),
			'Paginator': render_to_string('main/includes/Paginator.html', {'page': pageYear, 'page_range': pg })

		}



		return Response(data)


class LoadDefaultClients(APIView):
	authentication_classes 	= []
	permission_classes 		= []

	def get(self, request, *args, **kwargs) :
		today = date.today()
		qs			= Transaction.objects.all()
		qyear		= qs.filter(voucher__date__gte = today.replace(month=1, day=1), voucher__date__lte = today)
		qmonth		= qs.filter(voucher__date__gte = today - timedelta(days = 30), voucher__date__lte = today)
		qweek		= qs.filter(voucher__date__gte = today - timedelta(days = 7) , voucher__date__lte = today)


		for c in Client.objects.all():dic[c] = 0
		for i in qyear:dic[i.voucher.client] += i.amount
		serial 		= sorted(Client.objects.all(), key=cmp, reverse = True)
		yearTable 	= [(i, dic[i])  for i in serial]
		yearData	= [ dic[i] for i in serial]

		paginator = Paginator(yearTable, pageint)
		page = kwargs.get('page', 1)
		pg = proper_paginate(paginator, int(page))

		try:
			pageYear = paginator.page(page)
		except PageNotAnInteger:
			pageYear = paginator.page(1)
		except EmptyPage:
			pageYear = paginator.page(paginator.num_pages)


		for c in Client.objects.all():dic[c] = 0
		for i in qweek:dic[i.voucher.client] += i.amount
		serial 		= sorted(Client.objects.all(), key=cmp, reverse = True)
		weekTable 	= [(i, dic[i])  for i in serial]
		weekData	= [ dic[i] for i in serial]

		paginator = Paginator(weekTable, pageint)
		page = kwargs.get('page', 1)
		pg = proper_paginate(paginator, int(page))

		try:
			pageWeek = paginator.page(page)
		except PageNotAnInteger:
			pageWeek = paginator.page(1)
		except EmptyPage:
			pageWeek = paginator.page(paginator.num_pages)


		for c in Client.objects.all():dic[c] = 0
		for i in qmonth:dic[i.voucher.client] += i.amount
		serial 		= sorted(Client.objects.all(), key=cmp, reverse = True)
		monthTable 	= [(i, dic[i])  for i in serial]
		monthData	= [ dic[i] for i in serial]

		paginator = Paginator(monthTable, pageint)
		page = kwargs.get('page', 1)
		pg = proper_paginate(paginator, int(page))

		try:
			pagemonth = paginator.page(page)
		except PageNotAnInteger:
			pagemonth = paginator.page(1)
		except EmptyPage:
			pagemonth = paginator.page(paginator.num_pages)




		data = {
			'yearTable'		: render_to_string('main/includes/clientTable.html', {'page' : pageYear}),
			'yearData'		: yearData[pageYear.start_index()-1: pageYear.end_index()],
			'yearLabels'	: [' ']*(pageYear.end_index()- pageYear.start_index() + 1),
			'yearPaginator': render_to_string('main/includes/Paginator.html', {'page': pageYear, 'page_range': pg }),

			'weekTable'		: render_to_string('main/includes/clientTable.html', {'page' : pageWeek}),
			'weekData'		: weekData[pageWeek.start_index()-1: pageWeek.end_index()],
			'weekLabels'	: [' ']*(pageWeek.end_index()- pageWeek.start_index() + 1),
			'weekPaginator': render_to_string('main/includes/Paginator.html', {'page': pageWeek, 'page_range': pg }),

			'monthTable'	: render_to_string('main/includes/clientTable.html', {'page' : pagemonth}),
			'monthData'		: monthData[pagemonth.start_index()-1: pagemonth.end_index()],
			'monthLabels'	: [' ']*(pagemonth.end_index()- pagemonth.start_index() + 1),
			'monthPaginator': render_to_string('main/includes/Paginator.html', {'page': pagemonth, 'page_range': pg }),

		}



		return Response(data)



def loginView(request):
	if(request.method == 'GET'):
		return render(request, 'main/login.html',)

	print(request.POST)
	if(request.method == 'POST'):
		username = request.POST.get('username')
		password = request.POST.get('password')
		print(username)
		print(password)
		user = authenticate(request, username=username, password=password)
		if user is not None:
			login(request , user)
			return redirect('index')

	return redirect('login')




def logoutView(request):
	logout(request)
	return redirect('login')
